# 🖥️ PiForge Hardware Inventory

> Complete catalog of all Raspberry Pi hardware, accessories, and specifications for the home-pi-forge project.
> 
> **Last Updated:** April 24, 2026  
> **Status:** Hardware Assessment Phase — COMPLETE ✅

---

## 📋 Quick Summary

| Device | Model | Count | Status | Role |
|---|---|---|---|---|
| Raspberry Pi 5 | 8GB RAM | 3 | Assessed ✅ | Web Server, Database, Desktop Client |
| Raspberry Pi 4 | 4GB RAM | 1 | Assessed ✅ | Role TBD |
| Raspberry Pi Zero 2 W | 512MB RAM | 2 | Assessed ✅ | Status Display, Pi-hole DNS |
| Raspberry Pi Pico W | RP2040 | Multiple | Identified | Sensors |
| Raspberry Pi Pico | RP2040 | Multiple | Identified | Sensors |
| WEMOS D1 Mini | ESP8266 | 2 | Identified | IoT/Networking |

**Total Pis Deployed:** 6  
**Total Assessed:** 6  
**Total Identified:** 10+

---

## 🎯 Deployed Raspberry Pi Boards

### Pi #1 — Web Server: **pi-webserver**

| Property | Value |
|---|---|
| **Model** | Raspberry Pi 5 Model B Rev 1.0 |
| **Revision** | d04170 |
| **Serial Number** | 0997b2685e44ec6c |
| **CPU** | BCM2712 (4 cores) |
| **Max CPU Frequency** | 2400 MHz |
| **RAM** | 8GB |
| **Storage** | 58.9G microSD (mmcblk0) |
| **Used Storage** | 4.1G / 58G (8%) |
| **IP Address** | 192.168.4.138 |
| **Temperature** | 23.0°C |
| **Core Voltage** | 0.7200V |
| **OS** | Debian GNU/Linux 13 (trixie) |
| **Kernel** | 6.12.75+rpt-rpi-2712 |
| **Uptime** | 2 days, 1:39 |
| **Cooling** | None assigned yet |
| **HATs/Add-ons** | None |
| **Status** | Deployed and Running ✅ |

**Purpose:**
- Nginx reverse proxy
- Node.js / Express API
- Python data collector
- Java Spring Boot service
- Frontend dashboard

**Notes:**
- Running cool at 23°C
- Plenty of storage available on microSD
- Ready for Phase 1 (Web Server)

---

### Pi #2 — Database Server: **pi-database**

| Property | Value |
|---|---|
| **Model** | Raspberry Pi 5 Model B Rev 1.0 |
| **Revision** | d04170 |
| **Serial Number** | 15d4b260255757ed |
| **CPU** | BCM2712 (4 cores) |
| **Max CPU Frequency** | 2400 MHz |
| **RAM** | 8GB |
| **NVMe SSD** | **465.8GB** (nvme0n1) |
| **microSD** | 58.9G (mmcblk0) |
| **Used Storage (microSD)** | 4.1G / 58G (8%) |
| **Used Storage (NVMe)** | Minimal |
| **IP Address** | 192.168.4.139 |
| **Temperature** | 38.9°C |
| **Core Voltage** | 0.7200V |
| **OS** | Debian GNU/Linux 13 (trixie) |
| **Kernel** | 6.12.75+rpt-rpi-2712 |
| **Uptime** | 2 days, 1:36 |
| **Storage Adapter** | SAPI M.2 NVMe Adapter |
| **Cooling** | None assigned |
| **HATs/Add-ons** | SAPI M.2 NVMe Adapter |
| **Status** | Deployed and Running ✅ |

**Purpose:**
- PostgreSQL database server
- Persistent data storage
- Accessible over LAN

**Notes:**
- **465.8GB NVMe SSD** provides fast storage for database operations
- Running at comfortable 38.9°C
- Critical system — ensure regular backups
- Ready for Phase 2 (Database)

---

### Pi #3 — Admin/Connection Hub: **pi-nexus**

| Property | Value |
|---|---|
| **Model** | Raspberry Pi 4 Model B Rev 1.5 |
| **Revision** | c03115 |
| **Serial Number** | 10000000297cead3 |
| **CPU** | BCM2711 (4 cores) |
| **Max CPU Frequency** | 1800 MHz |
| **RAM** | 4GB |
| **Storage** | 58.9G microSD (mmcblk0) |
| **Used Storage** | 4.1G / 58G (8%) |
| **IP Address** | 192.168.4.25 |
| **Temperature** | 32.1°C |
| **Core Voltage** | 0.8700V |
| **OS** | Debian GNU/Linux 13 (trixie) |
| **Kernel** | 6.12.75+rpt-rpi-v8 |
| **Uptime** | Just booted (1 min) |
| **Cooling** | Active Cooling Case (with fans) |
| **HATs/Add-ons** | Active cooling case with integrated fans |
| **Status** | Deployed and Running ✅ |

**Purpose:**
- Role TBD (planning phase)
- Potential uses: monitoring, sensor aggregation, secondary services

**Notes:**
- Active cooling case keeps it at 32.1°C
- Good performance for supporting services
- Available for secondary workloads

---

## 📊 Client/Display Devices

### Workstation Status Display: **pi-beacon**

| Property | Value |
|---|---|
| **Model** | Raspberry Pi Zero 2 W Rev 1.0 |
| **Revision** | 902120 |
| **Serial Number** | 000000007037fc25 |
| **CPU** | RP3A0 (4 cores) |
| **Max CPU Frequency** | 1000 MHz |
| **RAM** | 512MB |
| **Storage** | 28.8G microSD (mmcblk0) |
| **Used Storage** | 2.3G / 28G (9%) |
| **IP Address** | 192.168.4.157 |
| **Temperature** | 44.0°C |
| **Core Voltage** | 1.2563V |
| **OS** | Raspbian GNU/Linux 13 (32-bit) |
| **Kernel** | 6.12.75+rpt-rpi-v7 |
| **Uptime** | Just booted (4 min) |
| **Display** | **Waveshare 2.13" e-Paper HAT** (SPI-connected) |
| **Cooling** | None |
| **Status** | Deployed and Running ✅ |

**Purpose:**
- Workstation status display
- Real-time system updates
- Low-power e-ink display

**Notes:**
- 32-bit OS optimized for 512MB RAM
- e-Paper display uses minimal power
- Perfect for desk-side monitoring
- SPI-connected display (not I2C)

---

### Desktop/Admin Client: **pi-desktop**

| Property | Value |
|---|---|
| **Model** | Raspberry Pi 5 Model B Rev 1.1 |
| **Revision** | e04171 |
| **Serial Number** | 5212cee48742851b |
| **CPU** | BCM2712 (4 cores) |
| **Max CPU Frequency** | Unknown (system dependent) |
| **RAM** | 16GB |
| **Storage** | 238.5G NVMe SSD (nvme0n1) |
| **Used Storage** | 18G / 235G (8%) |
| **Storage Adapter** | Raspberry Pi M.2 HAT+ (256GB) |
| **IP Address** | 192.168.4.13 |
| **Temperature** | 41.7°C |
| **OS** | Debian GNU/Linux 13 |
| **Uptime** | TBD |
| **Cooling** | None assigned |
| **HATs/Add-ons** | Raspberry Pi M.2 HAT+ with 256GB SSD |
| **Status** | In Use (Desktop Environment) |

**Purpose:**
- Raspberry Pi GUI/desktop environment
- Development and local administration
- Dashboard viewing

**Notes:**
- Highest RAM (16GB) in the fleet
- 238.5G NVMe SSD for fast OS and app performance
- Running cool at 41.7°C
- Role in PiForge: TBD (not yet assigned to specific phase)

---

## 🔧 Supporting/Utility Devices

### DNS/Ad-blocker: **pi-home**

| Property | Value |
|---|---|
| **Model** | Raspberry Pi Zero 2 W Rev 1.0 |
| **Revision** | 902120 |
| **Serial Number** | 0000000017ef4ea2 |
| **CPU** | RP3A0 (4 cores) |
| **Max CPU Frequency** | 1000 MHz |
| **RAM** | 512MB |
| **Storage** | 14.8G microSD (mmcblk0) |
| **Used Storage** | 3.6G / 15G (27%) |
| **IP Address** | 192.168.4.2 |
| **Temperature** | 52.1°C |
| **Core Voltage** | 1.2563V |
| **OS** | Raspbian GNU/Linux 12 (bookworm) |
| **Kernel** | 6.6.74+rpt-rpi-v7 |
| **Uptime** | **425 days** 🔥 |
| **Service** | **Pi-hole (DNS/ad-blocking)** |
| **Cooling** | None |
| **Status** | Deployed and Running ✅ |

**Purpose:**
- Network DNS/ad-blocker
- Pi-hole service
- Critical network service

**Notes:**
- **Impressive uptime: 425 days!** (Over 1 year without reboot)
- Running warm at 52.1°C due to continuous DNS filtering
- High load average (1.54, 1.32, 0.82) from query processing
- Critical — keep this running!
- Older OS (Bookworm) but stable

---

## 📦 Spare Hardware

| Device | Model | Specs | Serial | Status |
|---|---|---|---|---|
| Raspberry Pi Zero W | 512MB RAM, 1GHz | WiFi/Bluetooth | TBD | Identified, not yet assessed |

---

## 🔌 Microcontroller Boards

### Raspberry Pi Pico & Pico W

| Property | Value |
|---|---|
| **Count** | Multiple (exact count TBD) |
| **Processor** | RP2040 |
| **RAM** | 264 KB |
| **Flash Storage** | 2MB |
| **Connectivity** | WiFi/Bluetooth (Pico W only) |
| **Role** | Sensor data collection |
| **Firmware** | MicroPython |
| **Status** | Identified, not yet deployed |

---

### WEMOS D1 Mini (ESP8266)

| Property | Value |
|---|---|
| **Count** | 2 |
| **Processor** | ESP8266 |
| **RAM** | 160KB |
| **Flash Storage** | 4MB |
| **Connectivity** | WiFi (2.4GHz) |
| **Compatibility** | Arduino-compatible |
| **Role** | IoT/Networking/Sensors |
| **Status** | Identified, not yet deployed |

---

## 🎩 HATs & Expansion Boards

| Product | Model | Purpose | Status | Notes |
|---|---|---|---|---|
| **SAPI M.2 NVMe Adapter** | M.2 HAT+ | Fast storage for Pi 5 | **Deployed (pi-database)** | 465.8GB SSD installed |
| **Raspberry Pi M.2 HAT+** | M.2 HAT+ | Fast storage (256GB) | **Deployed (pi-desktop)** | 256GB SSD installed |
| **Raspberry Pi PoE+ HAT** | Official | Power over Ethernet (Pi 5) | Identified | With integrated fan and dual Ethernet |
| **Waveshare PoE HAT (E)** | Waveshare | Compact PoE (no fan) | Identified | Compact model, no active cooling |
| **Waveshare PoE HAT (F)** | Waveshare | Power over Ethernet (Pi 4) | Identified | With active cooling fan and dual Ethernet |
| **Waveshare 2.13" e-Paper HAT** | SPI Display | Status display for pi-beacon | **Deployed (pi-beacon)** | Low-power e-ink display |
| **Pirate Audio Speaker** | PIM485 | Audio output | Identified | I2S DAC, LCD display, buttons |
| **Pico Display Pack** | PIM543 | Display for Pico | Identified | 1.14" LCD, 240x135px, 4 buttons |

---

## 📺 Displays & Interfaces

| Device | Size/Spec | Purpose | Status | Attached To |
|---|---|---|---|---|
| Waveshare 2.13" e-Paper HAT | 2.13" e-ink | Status display | **Deployed** | pi-beacon |
| GeeekPi I2C 1602 LCD | 16x2 character | Data display | Identified | Available for sensors |

---

## 🔊 Sensors & Accessories

| Device | Model | Specification | Status |
|---|---|---|---|
| **Keyestudio 48-in-1 Sensor Kit** | 48-in-1 | 48 different sensors | Identified |

---

## 📊 Hardware Assessment Status

### ✅ Fully Assessed & Deployed

- [x] **pi-webserver** — Pi 5, Web Server role
- [x] **pi-database** — Pi 5 + 500GB NVMe, Database role
- [x] **pi-nexus** — Pi 4, role TBD
- [x] **pi-beacon** — Pi Zero 2 W + e-Paper display, Status display
- [x] **pi-home** — Pi Zero 2 W, Pi-hole DNS service
- [x] **pi-desktop** — Pi 5, Desktop client

### 🔄 Identified, Not Yet Assessed

- [ ] Raspberry Pi Zero W (spare)
- [ ] Multiple Raspberry Pi Pico W
- [ ] Multiple Raspberry Pi Pico
- [ ] 2x WEMOS D1 Mini

### 📋 Pending Deployment

- [ ] PoE+ HATs (all 3 models available)
- [ ] Pirate Audio Speaker (PIM485)
- [ ] Pico Display Pack (PIM543)
- [ ] GeeekPi I2C 1602 LCDs (2-pack)

---

## 🚀 Next Steps

1. **Role Assignment** — Finalize pi-nexus role
2. **Cooling Solution** — Consider cooling for pi-webserver
3. **Phase 1 Setup** — Begin Phase 1 Web Server deployment
4. **Phase 2 Setup** — PostgreSQL on pi-database
5. **Sensor Integration** — Deploy Picos and WEMOS boards

---

## 📝 Notes

- **Fleet Total:** 6 deployed Pis + multiple microcontrollers
- **Architecture:** Distributed (Web Server + Database + Utilities)
- **Storage:** Fast NVMe SSD for database, microSD for OS/apps
- **Cooling:** Mix of passive and active solutions available
- **Networking:** WiFi on most devices, PoE capable options available
- **Reliability:** Pi-home running 425+ days uninterrupted!

---

**Inventory last updated:** April 24, 2026  
**Next update:** After deploying Phase 1 and Phase 2

