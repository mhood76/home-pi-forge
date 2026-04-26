# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Home Pi Forge** is a phased home lab platform built on Raspberry Pi hardware. It covers a full stack — Nginx, Node.js/Express, Python, Java/Spring Boot, PostgreSQL, MicroPython sensors — deployed progressively across physical Pi nodes on a local network.

**GitHub:** https://github.com/mhood76/home-pi-forge

---

## Network Topology

All Pis are on the `192.168.4.x` subnet and reachable by hostname over SSH.

| Hostname | IP | Hardware | Role |
|---|---|---|---|
| `pi-webserver` | 192.168.4.138 | Pi 5 (8GB, microSD) | Nginx, Node.js, Express, Python, Java |
| `pi-database` | 192.168.4.139 | Pi 5 (8GB, 465GB NVMe) | PostgreSQL on NVMe SSD |
| `pi-desktop` | 192.168.4.13 | Pi 5 (16GB, 238GB NVMe) | Desktop / admin client |
| `pi-nexus` | 192.168.4.25 | Pi 4 (4GB, microSD) | Role TBD |
| `pi-beacon` | 192.168.4.157 | Pi Zero 2 W (512MB) | Waveshare 2.13" e-Paper HAT status display |
| `pi-home` | 192.168.4.2 | Pi Zero 2 W (512MB) | Pi-hole DNS / ad-blocking |

---

## Development Workflow

Code is written locally (on the dev machine) and deployed to Pis via git. **No Python, Node.js, or Java code in this repo can be run locally** — all scripts require Pi hardware (SPI, GPIO, `vcgencmd`, etc.) or LAN services.

```bash
# On dev machine: push changes
git push

# On the target Pi: pull and run
ssh user@pi-beacon.local
git -C ~/home-pi-forge pull
python3 pi-beacon/src/epaper_test.py
```

There is no test runner, linter, or build step configured in this repo.

---

## Common SSH Commands

```bash
# SSH into a Pi
ssh user@pi-webserver.local
ssh user@pi-database.local
ssh user@pi-beacon.local

# Service status checks
ssh user@pi-database.local "systemctl status postgresql"
ssh user@pi-webserver.local "systemctl status nginx"
ssh user@pi-home.local "pihole status"
```

---

## pi-beacon — e-Paper Display

`pi-beacon` runs a Pi Zero 2 W with a **Waveshare 2.13" e-Paper HAT V4** (250×122, B/W, SPI-connected). The display version is **V4** — confirmed by the label on the back of the panel. Using V2 or V3 drivers will silently fail (no error, no output).

### Setup (run on pi-beacon)

```bash
# System packages
sudo apt install python3-pip python3-pil python3-numpy python3-gpiozero libopenjp2-7 -y

# pip packages (--break-system-packages required on Pi OS 13+ due to PEP 668)
sudo pip3 install spidev setuptools waveshare-epd --break-system-packages

# Enable SPI: sudo raspi-config → Interface Options → SPI → Yes → reboot
# Verify: ls /dev/spi*  # should show /dev/spidev0.0 and /dev/spidev0.1
```

> **Note:** `pi-beacon/requirements.txt` lists `--break-system-packages` as a reminder only — pip cannot use it as a requirements file flag. Always install manually with the commands above.

### Running the test script

```bash
# Default (V4)
python3 pi-beacon/src/epaper_test.py

# Specify variant explicitly
python3 pi-beacon/src/epaper_test.py --variant V4

# Skip initial full clear during development
python3 pi-beacon/src/epaper_test.py --no-clear
```

### e-Paper display API lifecycle

Every display script must follow this exact sequence:

```python
from waveshare_epd import epd2in13_V4 as epd_module

epd = epd_module.EPD()
epd.init()                          # full refresh mode (default)
# epd.init(epd.PART_UPDATE)        # partial refresh mode

img = Image.new("1", (epd.width, epd.height), 255)  # 1-bit, white bg
draw = ImageDraw.Draw(img)
# ... draw with Pillow ...

epd.display(epd.getbuffer(img))     # full refresh
# epd.displayPartial(epd.getbuffer(img))  # partial refresh (faster, ghosting over time)

epd.sleep()                         # always sleep when done
```

### System font paths on Pi OS

```python
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
]
# Fall back to ImageFont.load_default() if none found
```

### e-Paper display rules
- Always call `epd.sleep()` when not updating — leaving the panel powered in a static state long-term damages it.
- Do a full refresh periodically when using partial refresh (`PART_UPDATE`) to prevent display artifacts.
- The ribbon cable ZIF connector must be fully seated with the locking tab flipped down on both ends.

---

## Phase Roadmap

| Phase | Focus | Stack |
|---|---|---|
| Phase 1 | Static web server | Linux, Nginx, HTML/CSS |
| Phase 2 | Database server | PostgreSQL, SQL |
| Phase 3 | Data collector | Python, psycopg2, cron |
| Phase 4 | REST API | Node.js, Express |
| Phase 5 | Dashboard | JavaScript, Chart.js |
| Phase 6 | Multi-device monitoring | SQL JOINs, MicroPython |
| Phase 7 | Auth | JWT, bcrypt, PostgreSQL |
| Phase 8 | Java microservice | Java, Spring Boot, Maven |
| Phase 9 | Public HTTPS | DDNS, Let's Encrypt, Nginx |

Each phase will live in its own directory (e.g. `phase1-webserver/`) with a `README.md` and a `.env.example` where secrets are needed.

---

## Python Version

Local Python version is pinned to **3.12.7** via `.python-version`.

---

## Key Architecture Notes

- **PostgreSQL lives exclusively on `pi-database`** — always connect on port 5432 over LAN.
- **Nginx on `pi-webserver`** acts as reverse proxy for all HTTP traffic (`/etc/nginx/` on the Pi).
- **Microcontroller code** (MicroPython for Pi Pico / Pico W, Arduino for WEMOS D1 Mini) will live under `/sensors/` or `/pico/` when added.
- **`pi-home`** runs Pi-hole with 425+ days uptime — treat it as critical, don't reboot unnecessarily.
- **`pi-beacon`** runs 32-bit Raspberry Pi OS (required for 512MB RAM) while all Pi 5s run 64-bit Debian 13.
