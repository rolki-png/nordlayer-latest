## Cursor Cloud specific instructions

This is an Arch Linux AUR packaging repo for NordLayer VPN. It contains:

- `PKGBUILD` / `.SRCINFO` / `nordlayer.install` — Arch Linux package build recipe and install hooks
- `update_pkgbuild.py` — Python 3 script that checks for new NordLayer releases, downloads the `.deb`, computes SHA-512, and updates `PKGBUILD` / `.SRCINFO`

### Running the Python update script

```
python3 update_pkgbuild.py
```

`generate_srcinfo()` in `update_pkgbuild.py` writes `.SRCINFO` from the PKGBUILD. It does not call `makepkg`.

`get_latest_version()` reads the `nordlayer` version from the Debian Packages index:

```
https://downloads.nordlayer.com/linux/latest/debian/dists/stable/main/binary-amd64/Packages
```

The help page is the next source. `https://downloads.nordlayer.com/linux/latest/version` still returns `3.3.2` from 2024, and that `.deb` returns 404.

### Lint checks

- **Shell scripts**: `bash -n PKGBUILD && bash -n nordlayer.install` for syntax; `shellcheck nordlayer.install` for style (SC2148 about missing shebang is expected — `.install` files are sourced by `makepkg`). Shellcheck warnings on `PKGBUILD` about "unused" variables are false positives (variables are consumed by `makepkg`).
- **Python**: `python3 -c "import py_compile; py_compile.compile('update_pkgbuild.py', doraise=True)"`

### Dependencies

Python 3 with `requests` and `beautifulsoup4` (installed via `pip3 install requests beautifulsoup4`).
