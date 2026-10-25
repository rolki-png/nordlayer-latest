import unittest

from update_pkgbuild import select_published_version, version_from_debian_packages


PACKAGES = """\
Package: nordlayer-tray
Version: 1.0.0
Architecture: amd64
Filename: ./pool/main/nordlayer-tray_1.0.0_amd64.deb

Package: nordlayer
Version: 3.6.0
Architecture: amd64
Filename: ./pool/main/nordlayer_3.6.0_amd64.deb
"""


class PublishedVersionTest(unittest.TestCase):
    def test_debian_index_names_nordlayer_not_the_tray_package(self):
        self.assertEqual(version_from_debian_packages(PACKAGES), "3.6.0")

    def test_debian_index_wins_over_the_stale_version_file(self):
        chosen = select_published_version(
            packages_version="3.6.0",
            help_version="3.5.0",
            file_version="3.3.2",
        )
        self.assertEqual(chosen, "3.6.0")

    def test_help_page_is_used_when_the_debian_index_is_missing(self):
        chosen = select_published_version(
            packages_version=None,
            help_version="3.6.0",
            file_version="3.3.2",
        )
        self.assertEqual(chosen, "3.6.0")

    def test_version_file_is_the_last_resort(self):
        chosen = select_published_version(
            packages_version=None,
            help_version=None,
            file_version="3.6.0",
        )
        self.assertEqual(chosen, "3.6.0")

    def test_blank_sources_return_none(self):
        self.assertIsNone(
            select_published_version(
                packages_version=None,
                help_version="",
                file_version="not-a-version",
            )
        )


if __name__ == "__main__":
    unittest.main()
