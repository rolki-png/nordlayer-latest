# [Nordlayer](https://nordlayer.com) VPN package for Linux (esp [ArchLinux](https://archlinux.org/))

[![AUR version](https://img.shields.io/aur/version/nordlayer)](https://aur.archlinux.org/packages/nordlayer) [![Nordlayer version](https://img.shields.io/badge/nordlayer-3.4.3-green)](https://nordlayer.com/download/linux/)

### Version tracking

The update script pulls the latest version from NordLayer's Debian repository metadata (the `Packages` index at `dists/stable/main/binary-amd64/Packages`). This is the primary source because it reflects exactly what's downloadable — the simple version API at `/linux/latest/version` can be stale and return versions whose `.deb` no longer exists.

HTML scraping of the help page and the version API are kept as fallbacks. Every candidate version is checked with a HEAD request against the `.deb` download URL before being accepted.

### Important

If you run into any errors feel free to create an [issue](https://github.com/raverecursion/nordlayer-latest/issues/new) or leave a comment [in AUR](https://aur.archlinux.org/packages/nordlayer-bin)

To check the version currently in the Debian repo:

```sh
curl -s https://downloads.nordlayer.com/linux/latest/debian/dists/stable/main/binary-amd64/Packages | grep -m1 '^Version:'
```

---

### Installing Nordlayer from AUR:

```sh
yay -S nordlayer-bin
```

### Building the package manually:

```sh
git clone https://github.com/raverecursion/nordlayer-latest.git
cd nordlayer-latest
makepkg -si
# If 'makepkg -si' fails to install automatically:
sudo pacman -U nordlayer-bin-3.2.2-1-x86_64.pkg.tar.zst
```

### Connection Error fix:

```
sudo usermod -a -G nordlayer $(whoami)
sudo setcap 'CAP_NET_ADMIN=+eip' /usr/libexec/nordlayer/nordlayer-charon
sudo setcap 'CAP_NET_ADMIN=+eip' /usr/libexec/nordlayer/nordlayer-ip
sudo setcap 'CAP_NET_ADMIN=+eip' /usr/libexec/nordlayer/nordlayer-openvpn
sudo setcap 'CAP_NET_ADMIN+eip CAP_DAC_OVERRIDE+eip CAP_SETUID+eip' /usr/libexec/nordlayer/nordlayer-resolvconf
sudo setcap 'CAP_NET_ADMIN=+eip' /usr/libexec/nordlayer/nordlayer-setcap
sudo setcap 'CAP_NET_ADMIN=+eip' /usr/bin/nordlayer
```

Remember to reboot after changes.
