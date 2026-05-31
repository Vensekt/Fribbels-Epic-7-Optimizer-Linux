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
# → release/FribbelsE7Optimizer_*_amd64.deb
```

## Rebuilding the Java backend

Upstream checks in a prebuilt `data/jar/backend.jar` that drifts behind
the Java source. When new gear sets get added to `Set.java` (e.g.
`WarfareSet`, `PursuitSet`), the stale JAR's Gson silently drops items
with the new set names during merge, and the optimizer kernel — also
compiled against the old enum — throws `RuntimeException` on Start.
Symptom: "scan reports N items, optimizer shows N-44 with the new sets
empty, optimizer crashes on Start."

To rebuild the JAR in place against its bundled dependencies:

```bash
sudo apt install -y openjdk-8-jdk
scripts/rebuild-backend.sh
```

The script recompiles every `com/fribbels/**/*.java` against the JAR's
existing dependency layer (gson, aparapi, guava, etc.) and splices the
new classes back in. Run it once after pulling source changes that
touch the backend, then `yarn package-linux` to refresh the AppImage.

## Run from source

```bash
yarn install
yarn dev      # in one terminal
yarn start    # in another
```

## Scanning from a phone (recommended setup)

Linux desktops with NetworkManager can host a Wi-Fi hotspot directly,
which avoids the need for an Android emulator entirely:

```bash
nmcli device wifi hotspot ssid E7Hotspot password "yourpassword123"
```

Connect your phone to that SSID, then start the scan and load Epic 7.

## Network interface selection

The bundled scanner sniffs TCP ports 5222 and 3333 for Epic 7 traffic.
On Linux the selection logic is:

1. If `FRIBBELS_SCAN_IFACE` env var is set, use that interface only.
2. Otherwise, prefer the first wireless interface found (`wl*`, `wlan*`,
   `wlp*`). This avoids double-capture when a Wi-Fi hotspot is active
   — the same phone-to-server stream appears once on the wireless iface
   (pre-NAT, with the phone's IP) and again on the upstream iface
   (post-NAT). Sniffing both interfaces feeds the parser interleaved
   streams it can't reassemble.
3. If no wireless iface is present, fall back to all non-virtual
   interfaces (skipping `lo`, `docker*`, `br-*`, `veth*`, `virbr*`,
   `tun*`, `tap*`).

To force a specific interface:

```bash
FRIBBELS_SCAN_IFACE=wlp3s0 ./FribbelsE7Optimizer-*.AppImage
```

Find your interfaces with `ip -br link`.

## What was changed for Linux

- `app/js/lib/files.js` — path separator handling no longer assumes
  non-Mac means Windows; added `isLinux()` / `isWindows()` helpers and
  a dedicated Linux branch in `getRootPath()`.
- `app/js/lib/ocr/ocr.js` — uses `path.sep` instead of hardcoded `\\`.
- `app/js/lib/scanner.js` — Linux-aware error dialog when no packets
  are captured.
- `data/py/scanner.py` — interface selection logic described above,
  plus surface sniff errors to stderr instead of swallowing them.
- `package.json` — Linux build target with `.desktop` entries (Game
  category, keywords) and icon registration so the deb/rpm/AppImage
  integrate with desktop environments.

The Java backend and Electron shell were already cross-platform.

## Known issues

- AppImage builds may need `--no-sandbox` on some distros (chrome-sandbox
  SUID issue). Workaround: `chmod u+s chrome-sandbox` inside the AppImage,
  or pass `--no-sandbox` at launch.
- If `setcap` is unset, Scapy will silently capture nothing — the
  no-data dialog will fire.
- If you have a wireless interface but the phone is connected to your
  router instead of a PC-hosted hotspot (i.e., the phone traffic isn't
  routed through your PC at all), set `FRIBBELS_SCAN_IFACE` to whichever
  interface your PC uses to reach the same subnet — sniffing your PC's
  Wi-Fi won't see traffic between phone and router.
