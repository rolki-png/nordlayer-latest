# Maintainer: Roland Kiraly <rolandgyulakiraly at outlook dot com>
# https://github.com/rolki-png/nordlayer-latest/tree/master
pkgname=nordlayer
pkgver=3.6.0
pkgrel=2
pkgdesc="Proprietary secure network access client for Linux"
arch=('x86_64')
url="https://nordlayer.com"
license=('custom:commercial')
replaces=('nordvpnteams-bin')
conflicts=('nordvpnteams-bin' 'nordlayer-bin')
depends=('bash' 'libgcrypt' 'libgpg-error' 'libcap' 'hicolor-icon-theme' 'gmp' 'strongswan')
options=('!strip' '!emptydirs')
install=${pkgname}.install
source_x86_64=("https://downloads.nordlayer.com/linux/latest/debian/pool/main/nordlayer_${pkgver}_amd64.deb")
sha256sums_x86_64=('037ff798826c3a453bd77b2ccd1e811c280a4205347a4a41a4f97791c3a3a9d2')

package() {
    cd "${srcdir}"
    # Extract the control and data tarballs from the .deb file
    ar x "${srcdir}/nordlayer_${pkgver}_amd64.deb"

    # Extract the data.tar.gz into the pkgdir
    tar -xzf data.tar.gz -C "${pkgdir}"

    # Move sbin binaries to bin
    if [ -d "${pkgdir}/usr/sbin" ]; then
        mv "${pkgdir}/usr/sbin"/* "${pkgdir}/usr/bin"
        # Update the systemd service file to point to /usr/bin instead of /usr/sbin
        sed -i 's+/usr/sbin+/usr/bin+g' "${pkgdir}/usr/lib/systemd/system/nordlayer.service"
        # Remove the now-empty sbin directory
        rm -r "${pkgdir}/usr/sbin"
    fi
}
