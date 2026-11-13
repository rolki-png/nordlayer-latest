# NordLayer for Arch Linux

Unofficial Arch packages for the NordLayer Linux client.

Maintained by Roland Kiraly. This started as a fork of [akumaburn/nordlayer-latest](https://github.com/akumaburn/nordlayer-latest), which has had no commits since February 2024, and has been rewritten since. A daily GitHub Actions job checks for new NordLayer releases and updates both packages, the update script has tests, and `nordlayer-bin` is new.

[![AUR version](https://img.shields.io/aur/version/nordlayer)](https://aur.archlinux.org/packages/nordlayer)

`nordlayer` and `nordlayer-bin` install the same client and conflict with each other. Install one of them.

## Install

```sh
yay -S nordlayer
```

The install script enables `nordlayer.service` and `nordlayer.socket`, starts both, and adds you to the `nordlayer` group. Log out and back in so the group applies. Then sign in.

```sh
nordlayer login
nordlayer connect
```

`nordlayer version` prints the version of the running client. `nordlayer status` shows whether you are logged in and connected.

## Build from this repo

```sh
git clone https://github.com/rolki-png/nordlayer-latest.git
cd nordlayer-latest
makepkg -si
```

## Report a problem

Open an [issue](https://github.com/rolki-png/nordlayer-latest/issues/new), or comment on the [nordlayer](https://aur.archlinux.org/packages/nordlayer) or [nordlayer-bin](https://aur.archlinux.org/packages/nordlayer-bin) AUR page.
