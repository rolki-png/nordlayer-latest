#!/usr/bin/env python3
"""Point both PKGBUILDs at the newest nordlayer .deb in NordLayer's Debian repo.

The repo's Packages index is the only source read. It names every published
version with its SHA-256, so the script never has to download the .deb, and a
rebuild that NordLayer publishes under an unchanged version gets a pkgrel bump.
"""

import os
import re
import sys
import urllib.request
from typing import NamedTuple

PACKAGES_URL = (
    'https://downloads.nordlayer.com/linux/latest/debian/'
    'dists/stable/main/binary-amd64/Packages'
)
PKG_DIRS = ['.', 'nordlayer-bin']
VERSION = re.compile(r'\d+(\.\d+)*')
SHA256 = re.compile(r'[0-9a-f]{64}')


class Release(NamedTuple):
    version: str
    sha256: str


class PkgState(NamedTuple):
    pkgver: str
    pkgrel: int
    sha256: str


def version_key(version):
    return tuple(int(part) for part in version.split('.'))


def releases_in_index(text):
    for block in re.split(r'\n\s*\n', text.strip()):
        fields = {}
        for line in block.splitlines():
            if line and not line[0].isspace() and ':' in line:
                key, value = line.split(':', 1)
                fields[key] = value.strip()
        if fields.get('Package') != 'nordlayer':
            continue
        version = fields.get('Version', '').split(':', 1)[-1].split('-', 1)[0]
        sha256 = fields.get('SHA256', '').lower()
        if VERSION.fullmatch(version) and SHA256.fullmatch(sha256):
            yield Release(version, sha256)


def latest_release(text):
    return max(releases_in_index(text), key=lambda r: version_key(r.version), default=None)


def read_state(pkgbuild):
    def field(pattern):
        match = re.search(pattern, pkgbuild, re.MULTILINE)
        if not match:
            raise ValueError(f'PKGBUILD has no line matching {pattern}')
        return match.group(1)

    return PkgState(
        pkgver=field(r'^pkgver=(\S+)$'),
        pkgrel=int(field(r'^pkgrel=(\d+)$')),
        sha256=field(r"^sha256sums_x86_64=\('([0-9a-f]{64})'\)$"),
    )


def next_state(current, release):
    if version_key(release.version) > version_key(current.pkgver):
        return PkgState(release.version, 1, release.sha256)
    if release.version == current.pkgver and release.sha256 != current.sha256:
        return PkgState(current.pkgver, current.pkgrel + 1, release.sha256)
    return None


def write_state(pkgbuild, state):
    for pattern, line in (
        (r'^pkgver=.*$', f'pkgver={state.pkgver}'),
        (r'^pkgrel=.*$', f'pkgrel={state.pkgrel}'),
        (r'^sha256sums_x86_64=.*$', f"sha256sums_x86_64=('{state.sha256}')"),
    ):
        pkgbuild = re.sub(pattern, line, pkgbuild, count=1, flags=re.MULTILINE)
    return pkgbuild


def fetch_index():
    request = urllib.request.Request(
        PACKAGES_URL, headers={'User-Agent': 'nordlayer-aur-updater'}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def main():
    release = latest_release(fetch_index())
    if release is None:
        sys.exit(f'No nordlayer package found in {PACKAGES_URL}')
    print(f'Upstream: {release.version} sha256 {release.sha256}')

    for pkg_dir in PKG_DIRS:
        path = os.path.join(pkg_dir, 'PKGBUILD')
        with open(path) as f:
            pkgbuild = f.read()
        current = read_state(pkgbuild)
        new = next_state(current, release)
        if new is None:
            print(f'{path}: {current.pkgver}-{current.pkgrel} is current')
            continue
        with open(path, 'w') as f:
            f.write(write_state(pkgbuild, new))
        print(f'{path}: {current.pkgver}-{current.pkgrel} -> {new.pkgver}-{new.pkgrel}')


if __name__ == '__main__':
    main()
