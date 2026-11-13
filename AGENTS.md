## Cursor Cloud specific instructions

This is an Arch Linux AUR packaging repo for NordLayer VPN. It contains:

- `PKGBUILD`, `.SRCINFO` and `nordlayer.install` hold the Arch Linux package build recipe and install hooks
- `update_pkgbuild.py` is a Python 3 script that uses only the standard library. It reads NordLayer's Debian Packages index and points both PKGBUILDs at the newest `nordlayer` `.deb` and its SHA-256
- `build-in-arch.sh` builds both packages with `makepkg` in an `archlinux:base-devel` container and rewrites each `.SRCINFO` from `makepkg --printsrcinfo`. Needs Docker

### Updating the packages

```
python3 update_pkgbuild.py
./build-in-arch.sh
```

The script's only source is the Packages index:

```
https://downloads.nordlayer.com/linux/latest/debian/dists/stable/main/binary-amd64/Packages
```

It picks the highest `nordlayer` version in the index. A newer version sets `pkgrel=1`. The same version with a new SHA-256 means NordLayer rebuilt the `.deb`, so `pkgrel` goes up by one. An older version is ignored. The CDN answers 403 to urllib's default User-Agent, so the script sends its own.

Never edit `.SRCINFO` by hand. After any PKGBUILD change, including a manual `pkgrel` bump, run `./build-in-arch.sh` and commit the `.SRCINFO` it writes.

### Running the tests

`python3 -m unittest -v` runs `test_update_pkgbuild.py`. The `Test` workflow runs it on pushes to `master` and on pull requests, builds both packages, and fails if a committed `.SRCINFO` differs from `makepkg --printsrcinfo`.

### Lint checks

- **Shell scripts**: `bash -n PKGBUILD && bash -n nordlayer.install` for syntax; `shellcheck nordlayer.install` for style. SC2148 about a missing shebang is expected, because `.install` files are sourced by `makepkg`. Shellcheck warnings on `PKGBUILD` about "unused" variables are false positives, because `makepkg` reads those variables.
