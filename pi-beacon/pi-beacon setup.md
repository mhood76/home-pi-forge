# 🟢 pi-beacon — Setup Log

> **Device:** Raspberry Pi Zero 2 W  
> **Role:** Workstation status display (e-Paper HAT)  
> **Display:** Waveshare 2.13" e-Paper HAT **V4** (250×122, Black/White)  
> **Last Updated:** 2026-04-24

---

## ✅ Step 1 — Fresh OS Install

|||
|---|---|
|**Date**|2026-04-24|
|**OS**|Raspberry Pi OS Lite 32-bit|
|**Hostname**|pi-beacon|

```bash
sudo apt-get update
sudo apt-get upgrade
```

---

## ✅ Step 2 — Enable SPI Interface

```bash
sudo raspi-config
# Interface Options → SPI → Yes → Finish
sudo reboot
```

**Verify SPI is active:**

```bash
ls /dev/spi*
# Expected output: /dev/spidev0.0  /dev/spidev0.1
```

---

## ✅ Step 3 — Install Python Dependencies

```bash
sudo apt install python3-pip python3-pil python3-numpy python3-gpiozero -y
sudo pip3 install spidev --break-system-packages
sudo pip3 install setuptools --break-system-packages
sudo apt install libopenjp2-7 -y
```

> **Note:** `--break-system-packages` is required on Raspberry Pi OS 13+ due to PEP 668 externally-managed-environment restrictions.

---

## ✅ Step 4 — GitHub Access

```bash
sudo apt install git gh -y

# Authenticate via browser
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser
# Follow the one-time code prompt

# Wire gh into git credential helper
gh auth setup-git
```

---

## ✅ Step 5 — Clone Project Repo

```bash
cd ~
git clone https://github.com/mhood76/home-pi-forge.git
```

---

## ✅ Step 6 — Verify Display Hardware

Clone the Waveshare demo library and run the matching example:

```bash
cd ~
git clone https://github.com/waveshare/e-Paper.git
cd e-Paper/RaspberryPi_JetsonNano/python/examples
python3 epd_2in13_V4_test.py
```

Once confirmed working, remove the demo library (already installed via pip):

```bash
rm -rf ~/e-Paper
```

> ⚠️ **Display Version Note:** This HAT is **V4** — confirmed by the label on the back of the e-Paper panel. V2 and V3 drivers will initialize without errors but nothing will appear on screen. Always verify the version label before selecting a driver.

---

## 📦 Installed Packages Summary

|Package|Method|Purpose|
|---|---|---|
|`python3-pip`|apt|Python package manager|
|`python3-pil`|apt|Image creation (Pillow)|
|`python3-numpy`|apt|Numerical arrays|
|`python3-gpiozero`|apt|GPIO abstraction|
|`libopenjp2-7`|apt|JPEG 2000 support for Pillow|
|`spidev`|pip|SPI device interface|
|`setuptools`|pip|Python package tooling|
|`git`|apt|Version control|
|`gh`|apt|GitHub CLI for auth|
|`waveshare-epd`|pip (e-Paper lib)|e-Paper display drivers|

---

## 🗒️ Notes & Gotchas

- **Don't clone `e-Paper` inside `home-pi-forge`** — clone it in `~` and remove after installing
- **Partial refresh warning:** e-Paper panels should not be partially refreshed indefinitely — do a full refresh periodically to prevent display artifacts
- **Sleep mode:** Always put the display to sleep when not updating — leaving it powered in a static state long-term can damage the panel
- **Ribbon cable:** ZIF connectors have a flip-up locking tab — cable must be fully seated and tab locked down on both ends