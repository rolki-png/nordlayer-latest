import unittest

from update_pkgbuild import (
    PkgState,
    Release,
    latest_release,
    next_state,
    read_state,
    write_state,
)

OLD_SHA = 'a' * 64
NEW_SHA = 'b' * 64

INDEX = f"""\
Package: nordlayer
Version: 3.6.0
Filename: ./pool/main/nordlayer_3.6.0_amd64.deb
SHA256: {OLD_SHA}

Package: nordlayer-tray
Version: 9.9.9
Filename: ./pool/main/nordlayer-tray_9.9.9_amd64.deb
SHA256: {'c' * 64}

Package: nordlayer
Version: 1:3.10.0-2
Filename: ./pool/main/nordlayer_3.10.0_amd64.deb
SHA256: {NEW_SHA}

Package: nordlayer
Version: 3.7.0
Filename: ./pool/main/nordlayer_3.7.0_amd64.deb
SHA256: {'d' * 64}
"""

PKGBUILD = f"""\
pkgname=nordlayer
pkgver=3.6.0
pkgrel=3
source_x86_64=("https://example.invalid/nordlayer_${{pkgver}}_amd64.deb")
sha256sums_x86_64=('{OLD_SHA}')
"""


class LatestReleaseTest(unittest.TestCase):
    def test_highest_nordlayer_version_wins_regardless_of_order(self):
        self.assertEqual(latest_release(INDEX), Release('3.10.0', NEW_SHA))

    def test_index_without_nordlayer_has_no_release(self):
        self.assertIsNone(latest_release('Package: nordlayer-tray\nVersion: 1.0.0\n'))


class NextStateTest(unittest.TestCase):
    current = PkgState('3.6.0', 3, OLD_SHA)

    def test_new_version_resets_pkgrel(self):
        self.assertEqual(
            next_state(self.current, Release('3.7.0', NEW_SHA)),
            PkgState('3.7.0', 1, NEW_SHA),
        )

    def test_rebuilt_deb_under_the_same_version_bumps_pkgrel(self):
        self.assertEqual(
            next_state(self.current, Release('3.6.0', NEW_SHA)),
            PkgState('3.6.0', 4, NEW_SHA),
        )

    def test_unchanged_upstream_needs_no_update(self):
        self.assertIsNone(next_state(self.current, Release('3.6.0', OLD_SHA)))

    def test_older_upstream_is_never_a_downgrade(self):
        self.assertIsNone(next_state(self.current, Release('3.5.0', NEW_SHA)))


class PkgbuildRoundTripTest(unittest.TestCase):
    def test_written_state_reads_back(self):
        new = PkgState('3.7.0', 1, NEW_SHA)
        rewritten = write_state(PKGBUILD, new)
        self.assertEqual(read_state(rewritten), new)
        self.assertIn('${pkgver}_amd64.deb', rewritten)


if __name__ == '__main__':
    unittest.main()
