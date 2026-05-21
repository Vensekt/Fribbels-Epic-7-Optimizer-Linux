# Linux support (experimental)

This branch adds native Linux compatibility to Fribbels E7 Optimizer.

## Prerequisites

```bash
# Debian / Ubuntu
sudo apt install openjdk-8-jre python3 python3-scapy libpcap0.8 nodejs yarn

# Fedora
sudo dnf install java-1.8.0-openjdk python3 python3-scapy libpcap nodejs yarn

# Arch
sudo pacman -S jre8-openjdk python python-scapy libpcap nodejs yarn
```

## Grant raw socket capability to Python

Scapy needs raw sockets to sniff game traffic. Instead of running the
optimizer as root, grant capability to the python binary:

```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(readlink -f $(which python3))
```

Verify:

```bash
getcap $(readlink -f $(which python3))
# → /usr/bin/python3.X cap_net_admin,cap_net_raw=eip
```

(Some distros use python-capsh wrappers — adjust accordingly.)

## Running the game

Epic 7 doesn't run natively on Linux. Use one of:

- **Waydroid** (Wayland-native Android container — recommended)
- **Genymotion** (commercial, x86 Android VM)
- **Anbox** (older but works)

When scanning, pick the bridge/tap interface that the emulator uses.

## Build

```bash
yarn install
yarn package-linux
# → release/FribbelsE7Optimizer-*.AppImage
```

## Run from source

```bash
yarn install
yarn dev      # in one terminal
yarn start    # in another
```

## What was changed for Linux

- `app/js/lib/files.js` — path separator handling no longer assumes
  non-Mac means Windows; added `isLinux()` / `isWindows()` helpers and
  a dedicated Linux branch in `getRootPath()`.
- `app/js/lib/ocr/ocr.js` — uses `path.sep` instead of hardcoded `\\`.
- `app/js/lib/scanner.js` — Linux-aware error dialog when no packets
  are captured.

The Java backend, Python scanner, and Electron shell were already
cross-platform.

## Known issues

- AppImage builds may need `--no-sandbox` on some distros (chrome-sandbox
  SUID issue). Workaround: `chmod u+s chrome-sandbox` inside the AppImage,
  or pass `--no-sandbox` at launch.
- If `setcap` is unset, Scapy will silently capture nothing — the
  no-data dialog will fire.
