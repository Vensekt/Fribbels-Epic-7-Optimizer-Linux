# Fribbels Epic 7 Gear Optimizer — Linux build

This is a Linux port of [fribbels/Fribbels-Epic-7-Optimizer](https://github.com/fribbels/Fribbels-Epic-7-Optimizer). All optimizer features on main are unchanged from upstream; this fork adds native Linux packaging (AppImage / .deb), Linux-specific packet-capture handling, and a rebuilt Java backend so newer gear sets (Warfare, Pursuit) import correctly.
The Experimental branch contains new features that haven't been thoroughly tested yet.

For Windows or macOS, use [the upstream project](https://github.com/fribbels/Fribbels-Epic-7-Optimizer) instead.

Please see the [**Getting Started**](#getting-started) section for instructions on how to use the optimizer.

Features include:
 - Automatically import gear and heroes from the game
 - Filter gear optimizer with main stats/sub stats/sets/etc
 - Automatic data updates for new heroes
 - Hero bonus stats for imprints/artifacts/EEs
 - Gear substat efficiency scoring
 - Reforged stat prediction & editing
 - Color coded results sorting
 - Substat modification optimization

Here's what it looks like currently:

![](https://i.imgur.com/vQ3tnol.png)

## Requirements

- 64-bit Linux (tested on Linux Mint / Ubuntu derivatives; the AppImage and `.deb` should work on any glibc-based distro)
- Java 8 (JRE) — for the optimizer's backend
  - Debian/Ubuntu/Mint: `sudo apt install openjdk-8-jre`
  - Fedora: `sudo dnf install java-1.8.0-openjdk`
  - Arch: `sudo pacman -S jre8-openjdk`
- Python 3 with `scapy`, plus `libpcap` — for the auto importer's packet capture
  - Debian/Ubuntu/Mint: `sudo apt install python3 python3-scapy libpcap0.8`
  - Fedora: `sudo dnf install python3 python3-scapy libpcap`
  - Arch: `sudo pacman -S python python-scapy libpcap`
- A way to route Epic 7's traffic through your PC (any one of):
  - An Android emulator on the same machine (Waydroid recommended)
  - A Wi-Fi hotspot hosted by your PC, with your phone connected to it

The full Linux installation walkthrough lives in [`LINUX.md`](LINUX.md).

_________________

- [Fribbels Epic 7 Gear Optimizer](#fribbels-epic-7-gear-optimizer)
  * [Requirements](#requirements)
  * [Optimizer Tab](#optimizer-tab)
    + [Settings panel](#settings-panel)
    + [Stat filters](#stat-filters)
    + [Rating filters](#rating-filters)
    + [Substat priority filter](#substat-priority-filter)
    + [Main stat and set filters](#main-stat-and-set-filters)
    + [Optimization Results](#optimization-results)
  * [Gear Tab](#gear-tab)
    + [Gear score](#gear-score)
  * [Heroes Tab](#heroes-tab)
    + [Adding bonus stats](#adding-bonus-stats)
    + [Substat modification options](#substat-modification-options)
  * [Importer tab](#importer-tab)
    + [Save or Load all optimizer data](#save-or-load-all-optimizer-data)
  * [Getting Started](#getting-started)
    + [Installing the app](#installing-the-app)
    + [Setting up the auto importer](#setting-up-the-auto-importer)
    + [Using the auto importer](#using-the-auto-importer)
        * [From an Android emulator (Waydroid)](#from-an-android-emulator-waydroid)
        * [From a phone via a PC-hosted Wi-Fi hotspot](#from-a-phone-via-a-pc-hosted-wi-fi-hotspot)
    + [Optimizing a unit](#optimizing-a-unit)
    + [Updating your gear](#updating-your-gear)
    + [Tips to get good optimization results](#tips-to-get-good-optimization-results)
  * [Troubleshooting](#troubleshooting)
    + [Automatic importer troubleshooting](#automatic-importer-troubleshooting)
    + [Optimizer troubleshooting](#optimizer-troubleshooting)
  * [Contributing to the project](#contributing-to-the-project)
    + [Setup steps](#setup-steps)

## Optimizer Tab

Here I'll go through the different parts of the optimizer tab, using a tank Ruele build as an example. There are a bunch of panels with options for filtering the gear that I'll walk through in detail.

_________________

### Settings panel

![](https://i.imgur.com/eIWkJ09.png)

This panel tracks settings for the other panels to use.

- **Hero**: Select the hero you want to optimize for from the drop down.
  - **Start**: Click to start to optimization request.
  - **Filter**: Once an optimization is complete, click to filter the results by the stats on the filter panels.
  - **Cancel**: Interrupts and cancels an ongoing optimization request.
  - **Load settings**: Loads the optimization settings from the last search for this hero.
  - **Reset settings**: Sets all optimization settings to their default values.
- **Stats**: Preview the hero's current stats on the left vs the new stats on the right.
- **Options**: Change options for optimizing your hero
  - **Use reforged stats**: Predict the reforged stats on +15 level 85 gear to use in the search.
  - **Use substat mods**: Run the optimization using substat modification stones. Each hero's optimization settings must first be selected on the heroes tab before this can be used.
  - **Only maxed gear**: When checked, only use +15 gear that cannot be further upgraded/reforged.
   - **Locked items**: When checked, locked items will be used in the optimization. When unchecked, locked items are ignored.
  - **Equipped items**: When checked, equipped items will be used in the optimization. When unchecked, equipped items are ignored EXCEPT for the unit's own equipped items.
  - **Keep current**: When checked, the unit will be forced to use the gear that it currently has, and the optimizer will only try to optimize the gear slots that the unit has unequipped.
  - **Exclude Equipped**: Select the heroes whose gear you want to be ignored in the optimization search. Add finished heroes to this list so other heroes can't steal their gear. Only works when 'Equipped items' is checked.

_________________

### Stat filters

![](https://i.imgur.com/9VPlYjo.png)

This panel defines the stats to filter your optimization results by. The left boxes are the minimum (inclusive) and the right boxes are the maximum (inclusive). In this example, we're looking for a build with:
- At least 20,000 HP
- At least 2,400 def
- Between 180 and 200 speed

The filter will apply on your optimization results after you click Submit. Once the results have been generated, you can apply more restrictive filters by changing the numbers here, then clicking the **Filter** button. This will narrow down your results without having to do another search.
_________________

### Rating filters

![](https://i.imgur.com/VvNA4ca.png)

This panel is similar to the primary stats panel, but applies for calculated stats. These stats you won't see in-game but are various ratings that can help decide between different builds.

- **HpS** -- `Health * Speed` rating. Useful for optimizing units where you want a combination of speed and pure health.
- **Ehp** -- Effective HP, calculated by: `HP * (Defense/300 + 1)`. EHP is a measure of how much damage your unit can take before dying and is useful for rating the tankiness of units.
- **EhpS** -- `Effective HP * Speed` rating. Useful for optimizing units where you want a combination of speed and hp/def for tankiness.
- **Dmg** --  Average damage, calculated by: `Attack * Crit Chance * Crit Damage`. Measures how much damage your unit will deal on average. Note that this takes crit chance into account, so lowering your crit chance impacts the Dmg rating because you'll crit less often, which lowers your average output.
- **DmgS** -- DPS rating, calculated by: `Attack * Crit Chance * Crit Damage * Speed`. This measures how fast your unit can dish out damage.
- **Mcd** -- Max Crit Damage, calculated by: `Attack * Crit Damage`. This does not take into account Crit Chance, as opposed to Dmg, and assumes your unit is at 100% Crit Chance. Useful for measuring damage of units like CDom that only need 50% Crit Chance, or PVE units that only need 85% with elemental advantage.
- **McdS** -- Max DPS rating, calculated by `Attack * Crit Damage * Speed`. Similar to DmgS, just without Crit Chance.
 - **DmgH** -- Bruiser rating, calculated by `Health * Crit Damage`. Useful for health scaling bruisers.
- **CP** -- This is the CP you would see on the unit's stat page ingame, but doesn't take skill enhances into account. Useful for optimizing unused characters with leftover gear for world boss.
_________________

### Substat priority filter

![](https://i.imgur.com/w55RbpG.png)

**This is probably the most useful filter but please read before using it. Using this wrong can exclude good results from the search.**

Assign a priority to each substat type from -1 to 3. This will go through every gear, and calculates the # of max rolls of each stat. The # of rolls is then multiplied by the stat priority you chose. It adds up all the stat scores for a gear, and sorts your gear by their highest substat score.

 In this example we're mostly looking for a fast and tanky Ruele so we assign:
- HP and Def a high rating of 3, since those are the highest priority stats
- Speed a slightly lower rating of 2
- And Res a rating of 1, as it's a nice-to-have stat and can still be useful for her
- We don't particularly care about Attack/Crit Chance/Crit Damage/Effectiveness, so we leave those at 0

Then, we set the Top % slider to 30%. This will take all your weapons, score them based on the priority defined above, then only considers the Top 30% of the scores for optimization. Then it does the same for helmets, armors, etc, and then the optimizer generates permutations based on those Top 30% gears.

**The Top % slider must be set to something other than 100% for this filter to work**, otherwise you're just using the Top 100% of your gears and nothing is being filtered. Worth noting that this rating is a heuristic so it doesn't always produce optimal results if your percent is set too low. I find that 30-50% is a good range to work with, because 50% filters out most of the irrelevant gears (like dps stats on a tank build, or vice versa). Below 30%, the filter gets very sensitive and you might not have enough gears to produce optimal results, so the results can be missing some permutations when some useful gears get filtered out. Try playing around with different Top % values.

An example priority filter for a DPS unit like Arby could be something like this, where you only want damage stats:

![](https://i.imgur.com/iy4A8d2.png)

Or for a tanky Champion Zerato, where you want a mix of tankiness, damage, and effectiveness, but NOT resistance, you can set resistance to -1 to decrease the gear rating if it has resist substats:

![](https://i.imgur.com/idsnxVW.png)

Choosing a good priority filter makes the optimization a lot easier since you won't have to consider irrelevant or low-rolled gears.

_________________

### Main stat and set filters

![](https://i.imgur.com/NPsmTVw.png)

This one's fairly straightforward, we're looking for:
- Necklaces with Health % OR Defense %
- Rings with Health % OR Defense %
- Boots with Speed
- Speed set
- Resist set OR immunity set

If we don't care about sets as much for a tanky/damage ML Ken or something, this allows for broken sets as well. Here we only care that he has an immunity set, and no preference for any other sets, so they're left blank.

![](https://i.imgur.com/zDcMb1A.png)

_________________

### Optimization Results

![](https://i.imgur.com/qxzV1HS.png)

Here you can see all the results from the optimization, sort by stat, and equip/lock the results.
- The top row shows your currently equipped gear stats
- Each column is color coded based on the min/max ranges of the stat on each page
- You can use the arrows at the bottom to navigate between multiple pages of results
- Select All/Deselect All modifies the little checkbox on each gear, or alternatively you can click individual boxes
- Equip Selected will equip those checked gears onto the hero (while unequipping anything they were holding before)
- Lock Selected will mark those checked gears as locked, which affects later optimizations that have "Locked Items" unchecked in settings.
- Clicking on the pencil/hammer icons will allow you to edit/reforge item stats.

## Gear Tab

![](https://i.imgur.com/hEjsPOJ.png)

Here you can find a table of all your gears, and sort/filter them. The icons at the bottom enable filters for set and gear slot, and the X clears the filters.

### Gear score

The **Score** column is a stat I made up which is similar to WSS, with the difference that it takes flat stats into consideration while WSS ignores them. The calculation is:

    Score = Attack %
    + Defense %
    + Hp %
    + Effectiveness
    + Effect Resistance
    + Speed * (8/4)
    + Crit Damage * (8/7)
    + Crit Chance * (8/5)
    + Flat Attack * 3.46 / 39
    + Flat Defense * 4.99 / 31
    + Flat Hp * 3.09 / 174

It's used as a measure of how well your gear rolled, scaled by the max roll for 85 gear (using max of 4, not 5 for speed). I found the average rolls for flat stats and compared it to the average stats of a base 5* unit at max level, and used that as a measure of how well the flat stats rolled. (For example, average roll flat def is 31, while the average flat def roll is worth 4.99% def on the average unit)

The other scores on this page are defined as:
* dScore - DPS Score. This is the Score formula but only counting Attack/%, Crit Chance, Crit Damage, and Speed
* sScore - Support Score. This is the Score formula but only counting Hp/%, Defense/%, Effect Resist, and Speed
* cScore - Combat Score. This is the Score formula excluding Effectiveness and Effect Resist


![](https://i.imgur.com/L3pbMp6.png)

You can edit existing gears or add new gears with the *Equip / Edit Item* button, and filling in the relevant fields on this page.

## Heroes Tab

![](https://i.imgur.com/B7tupLX.png)

Here you can add new heroes and manage existing ones. The second grid saves a history of your past builds. The bottom shows your currently selected builds on the hero.

### Adding bonus stats

The **Add Bonus Stats** button lets you add artifact/imprint/exclusive equipment stats to the hero for optimization.

![](https://i.imgur.com/0yFNcBK.png)

### Substat modification options

The **Add Substat Mods** button lets you customize the hero's settings when optimizing with substat mods enabled.

![](https://i.imgur.com/wxUsDWI.png)

The substat selections menu allows you to drag substats from the *Don't change* column to either *Wanted* or *Unwanted*. Unwanted substats will be converted into Wanted substats, which the Don't change ones will not be modified or selected for in the results.

* **Options**
  * Limit rolls - Choose the maximum number of rolls to replace. For example, limit rolls = 1 would only replace base stats that didn't get enhanced. It is generally not a good idea to replace more than 2 rolls, and the higher this number is, the more permutations will be generated.
  * Mod grade - Choose whether to use Greater or Lesser gem stats.
  * Roll quality - Choose the modified substat's roll value, from min roll to max roll. The actual value ingame will be random. Values will be rounded to the nearest whole number.
  * Wanted stats - Choose whether wanted stats should be allowed to be replaced with wanted stats when optimizing. For example, when allowed, a min speed roll could be replaced by a max speed roll. When not allowed, the speed will be left unmodified.
- **Tips for using substat mods**
  - Each substat change is considered as a new item, so you will have to increase your Top % and wait longer for good results
  - Selecting fewer "wanted substats" and "unwanted substats" will make the optimization faster because it generates less permutations
  - Searching multiple billion permutations is not uncommon when substats mods are enabled. Locking items and using the hero priority filter/etc can help reduce the search space
  - The optimizer is only meant to show modification possibilities, but its not always a good idea to modify certain items for a specific build. Choose wisely
  - Each substat change is considered an upgrade, and can be filtered for with the "Upg" filter, if you only want to modify 1-2 items for example**

## Importer tab

![](https://i.imgur.com/Ze2db9H.png)

This tab lets you do various things with importing/exporting files.
_________________

### Save or Load all optimizer data

Once you make changes to your items/heroes, the changes should be saved before you close the app. You can choose a file to save it to, and then later on load that file to import the data back in.

The app also does autosave to an 'autosave.json' upon changes being made, and will autoload whatever was saved to the autosave file the next time the app opens.

## Getting Started

### Installing the app

Pick one of the following:

**AppImage (works on any glibc distro):**

1. On the [Releases](https://github.com/Vensekt/Fribbels-Epic-7-Optimizer-Linux/releases) page, download `FribbelsE7Optimizer-x.x.x.AppImage`.
2. Make it executable and run it:
   ```bash
   chmod +x FribbelsE7Optimizer-*.AppImage
   ./FribbelsE7Optimizer-*.AppImage
   ```
3. (Optional) If your distro rejects the bundled chrome-sandbox, launch with `--no-sandbox`.

**Debian / Ubuntu / Mint package:**

1. Download `FribbelsE7Optimizer_x.x.x_amd64.deb` from the [Releases](https://github.com/Vensekt/Fribbels-Epic-7-Optimizer-Linux/releases) page.
2. Install:
   ```bash
   sudo apt install ./FribbelsE7Optimizer_*_amd64.deb
   ```
3. Launch from your application menu, or run `fribbelse7optimizer` from a terminal.

**From source:** see [`LINUX.md`](LINUX.md) for the full build recipe.

After installation, install the JRE if you haven't already — see [Requirements](#requirements).

_________________

### Setting up the auto importer

The automatic importer captures Epic 7's network traffic via Python + Scapy. Two one-time setup steps are required:

1. **Install Python 3 + Scapy + libpcap** (see [Requirements](#requirements) for the per-distro command).

2. **Grant raw-socket capability to Python** so Scapy can sniff without running as root:
   ```bash
   sudo setcap cap_net_raw,cap_net_admin=eip $(readlink -f $(which python3))
   ```
   Verify:
   ```bash
   getcap $(readlink -f $(which python3))
   # → /usr/bin/python3.X cap_net_admin,cap_net_raw=eip
   ```

If `setcap` is missing, Scapy will silently capture nothing and the importer will report no data.

### Using the auto importer

You can run the auto importer against either an Android emulator on the same machine or a real phone routed through your PC.

##### From an Android emulator (Waydroid)

1. Install [Waydroid](https://docs.waydro.id/usage/install-on-desktops) and install Epic 7 inside it.
2. With the optimizer open, click **Start scanning**.
3. Launch Epic 7 in Waydroid and load into the lobby.
4. (Optional) Open the storage menu and wait ~5 seconds — this is what makes your storage items show up in the import.
5. Click **Stop scanning**.
6. Wait up to 30 seconds. When the gear data appears, click **Export** to save it as `gear.txt`.
7. Click **Merge** and select that `gear.txt`.
8. On the Gear tab, use the **Level = 0** filter to fix any items the scanner couldn't fully parse.

##### From a phone via a PC-hosted Wi-Fi hotspot

NetworkManager-based desktops can host a Wi-Fi hotspot directly:

```bash
nmcli device wifi hotspot ssid E7Hotspot password "yourpassword123"
```

Then:

1. Connect your phone to the `E7Hotspot` SSID.
2. In the optimizer, click **Start scanning**.
3. Open Epic 7 on the phone and load into the lobby (open storage if you want storage items imported).
4. Click **Stop scanning**.
5. Continue with steps 6–8 from the emulator instructions above.

If you have multiple network interfaces and the scanner picks the wrong one, force it with the `FRIBBELS_SCAN_IFACE` env var — see [`LINUX.md` § Network interface selection](LINUX.md#network-interface-selection).

_________________

### Optimizing a unit

1. Add a unit on the Heroes tab, by selecting their name and clicking Add New Hero.
2. Select the new hero and click Add Bonus Stats. Here add any stats from your artifact, imprint, or EE. [Example](https://i.imgur.com/2aC22mN.png)
3. Go to the Optimizer tab, then select the hero. Fill in the main stats and set that you want into the right panel. [Example](https://i.imgur.com/3yfbkrE.png)
4. Fill in any filters you would like to apply. Each filter is described in detail in this section: https://github.com/fribbels/Fribbels-Epic-7-Optimizer#optimizer-tab
5. Hit Submit, and after processing a bit you should see a table of results.
6. Navigate the results with your arrow keys or mouse, select the result you want, and click Equip Selected.
7. You should now see your hero using those gears.
8. If you want to manually equip a certain item on a unit, go to the Gear tab -> Edit Selected Item -> Equipped. [Example](https://i.imgur.com/Bqs3ETL.png)

Here's a video that covers most of the importing process: https://www.youtube.com/watch?v=i_QW4INcZIE

_________________

### Updating your gear

* After enhancing/reforging/modifying your gear, you'll need to update it in the optimizer
* Run the auto importer again to generate a new gear.txt
* Use the Merge button on the Importer tab to update your existing save with the new gear

_________________

### Tips to get good optimization results

Here's some quick tips on getting the best results. This is assuming you've read the [Optimization panel](https://github.com/fribbels/Fribbels-Epic-7-Optimizer#optimizer-tab) descriptions.

* **Input the sets and main stats whenever possible.** This is the easiest way to narrow down results.
* **Use the substat priority filter and make sure to set your stat priority correctly!**
  * DPS units should have high priority on Atk / Cr / Cd / Speed for example.
  * Tank units should have high priority on Hp / Def / Speed for example.
  * Bad priorities will lead to bad results because good options get filtered out.
* **Lower the Top % to make the search faster, or increase Top % to search more results.** Most of the time I use 20-30%, sometimes lower if I want only my best gear on the unit.
* If you want a certain piece of gear to stay on a hero, go to the Gear tab -> Edit Selected Item -> Equipped and equip it on them first. [Example](https://i.imgur.com/oNO9ivL.png) Then you can use the optimizer with "Keep current" checked to keep that piece on them.

_________________

## Troubleshooting

### Automatic importer troubleshooting

* **No data captured / importer hangs past 30 seconds**
  * Verify Python has packet-capture capability:
    ```bash
    getcap $(readlink -f $(which python3))
    # Expect: cap_net_admin,cap_net_raw=eip
    ```
    If empty, re-run the `setcap` step from [Setting up the auto importer](#setting-up-the-auto-importer).
  * Verify Scapy is installed against the python3 you setcap'd:
    ```bash
    python3 -c "import scapy; print(scapy.__version__)"
    ```
  * Confirm the game traffic is actually reaching your PC. With Epic 7 running on the phone/emulator:
    ```bash
    sudo tcpdump -i any -n 'tcp and (port 3333 or port 5222)' -c 20
    ```
    If you see no packets, the phone isn't routing through your PC (it may be on mobile data, or your hotspot dropped the route).
  * Launch the AppImage from a terminal and watch stderr for `scanner: sniffing on [...]` or `scanner: sniff failed: ...`.

* **Scanner picks the wrong network interface**
  * The scanner auto-prefers wireless interfaces (`wl*`, `wlan*`, `wlp*`) and falls back to all non-virtual interfaces. To force a specific one:
    ```bash
    FRIBBELS_SCAN_IFACE=wlp3s0 ./FribbelsE7Optimizer-*.AppImage
    ```
    Find your interfaces with `ip -br link`.

* **VPN active** — disable it before scanning; the encrypted tunnel will hide Epic 7's traffic from Scapy.

* **Imported fewer items than your in-game inventory** — make sure you opened the storage menu in the lobby and waited a few seconds before stopping the scan. The game only streams storage items when storage is opened.

### Optimizer troubleshooting

- **"Subprocess error" / "Optimization request failed" when you click Start**
  - This means the backend JRE isn't reachable. Confirm Java 8 is installed and on PATH:
    ```bash
    java -version
    ```
  - If you built from source and updated the Java code, you may also need to rebuild the bundled JAR — see [`LINUX.md` § Rebuilding the Java backend](LINUX.md#rebuilding-the-java-backend).

- **"Java process failed" / "Unable to load Java" the moment you click Optimize**
  - The Java backend is segfaulting inside the OpenCL driver during aparapi's GPU kernel teardown. Confirm by checking for a JVM crash log next to the AppImage (`hs_err_pid*.log`) — the offending frame will be `libOpenCL.so.1` → `clReleaseCommandQueue`, with `com.aparapi.*` Java frames above it. Earlier alerts usually show `clBuildProgram failed` / `clCreateKernel() failed invalid program`, meaning your OpenCL ICD can't compile aparapi's kernels in the first place.
  - **Fix:** disable GPU acceleration in the **Settings** tab and click Optimize again. This is a driver-compatibility problem (common with Mesa rusticl, Intel Compute Runtime, and some ROCm builds), not a bug in the optimizer — aparapi's OpenCL 1.x kernels don't compile cleanly on every Linux GPU stack. The CPU path is plenty fast for normal use.
  - If you want to keep GPU acceleration, try installing POCL as a fallback ICD (`sudo apt install pocl-opencl-icd`) and force it for the session with `OCL_ICD_VENDORS=/etc/OpenCL/vendors/pocl.icd ./FribbelsE7Optimizer-*.AppImage`. `clinfo` will show which ICDs are visible.

- **AppImage refuses to launch with a chrome-sandbox / SUID error**
  - Run with `--no-sandbox`:
    ```bash
    ./FribbelsE7Optimizer-*.AppImage --no-sandbox
    ```
  - Or extract the AppImage and `chmod u+s` the bundled `chrome-sandbox` binary.

- **Newest gear sets (Warfare, Pursuit) show 0 items after a successful scan**
  - This is the stale-JAR symptom — upstream's bundled `backend.jar` predated those sets. The Linux build ships a rebuilt JAR that includes them; if you're running from a stale source checkout, re-run `scripts/rebuild-backend.sh` and rebuild the AppImage.

- **Duplicate-looking rows in the optimizer results**
  - You probably have actual duplicate gear in your DB. [Example](https://i.imgur.com/hUcyN1I.png)
  - Use the **Duplicates** filter on the Gear tab to find and fix them. Prefer **Merge** over **Append** when re-importing, since Append can create duplicates.

## Contributing to the project

The E7 optimizer is currently in maintenance mode - I'll be keeping the project updated with new units but all new feature development is on pause.

