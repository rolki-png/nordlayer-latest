#!/bin/bash
# Build nordlayer and nordlayer-bin with makepkg in an Arch Linux container,
# then rewrite each .SRCINFO from makepkg --printsrcinfo.
# Run from the repository root. Needs Docker.
set -euo pipefail

if [ "${1:-}" != --inside ]; then
  exec docker run --rm -e HOST_UID="$(id -u)" -v "$PWD:/repo" \
    archlinux:base-devel bash /repo/build-in-arch.sh --inside
fi

useradd -m -u "$HOST_UID" builder
for dir in /repo /repo/nordlayer-bin; do
  su builder -c "cd '$dir' && makepkg --printsrcinfo > .SRCINFO"
  su builder -c "cd '$dir' && SRCDEST=/tmp/src BUILDDIR=/tmp/build PKGDEST=/tmp/out makepkg -fd --noconfirm"
done
for pkg in /tmp/out/*.pkg.tar.zst; do
  bsdtar -tf "$pkg" | grep -qx 'usr/bin/nordlayerd' || { echo "$pkg has no usr/bin/nordlayerd" >&2; exit 1; }
done
ls -l /tmp/out
