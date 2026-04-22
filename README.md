# 🔥 Home Pi Forge

> A progressively built home lab platform — sensors, databases, APIs, dashboards, and beyond — running entirely on Raspberry Pi hardware.

Home Pi Forge is a personal home lab project that grows phase by phase from a simple web server into a full-stack, multi-language, publicly accessible web platform. Each phase builds directly on the last, covering Python, JavaScript, Node.js, PostgreSQL, Java, and more — all running on real hardware you own.

---

## 🏗️ Architecture

```
┌─────────────────────────────┐        ┌──────────────────────────────┐
│     Pi #1 — Web Server      │        │    Pi #2 — Database Server   │
│                             │        │                              │
│  • Nginx (reverse proxy)    │◄──────►│  • PostgreSQL on SSD         │
│  • Node.js / Express API    │        │  • Persistent data storage   │
│  • Python data collector    │        │  • Accessible over LAN       │
│  • Java Spring Boot service │        │                              │
│  • Frontend dashboard       │        └──────────────────────────────┘
└─────────────────────────────┘
            ▲
            │
┌─────────────────────────────┐
│     Pi Pico(s) — Sensors    │
│                             │
│  • MicroPython              │
│  • Temperature, humidity,   │
│    and other sensor data    │
│  • Low power, always-on     │
└─────────────────────────────┘
```

---

## 📍 Phase Roadmap

| Phase | Focus | Key Technologies |
|-------|-------|-----------------|
| [Phase 1 — Web Server](./phase1-webserver/) | Serve a static site on your local network | Linux, Nginx, HTML/CSS |
| [Phase 2 — Database](./phase2-database/) | Set up PostgreSQL on a dedicated Pi with SSD | PostgreSQL, SQL |
| [Phase 3 — Data Collector](./phase3-data-collector/) | Log Pi health stats to the database | Python, psycopg2, cron |
| [Phase 4 — REST API](./phase4-api/) | Expose database data via a REST API | Node.js, Express, npm |
| [Phase 5 — Dashboard](./phase5-dashboard/) | Live charts powered by the API | JavaScript, Chart.js |
| [Phase 6 — Multi-Device](./phase6-multi-device/) | Monitor both Pis, add Pico sensor data | SQL JOINs, MicroPython |
| [Phase 7 — Auth](./phase7-auth/) | Add user login and protected routes | JWT, bcrypt, PostgreSQL |
| [Phase 8 — Java Service](./phase8-java-service/) | Add an alerting microservice in Java | Java, Spring Boot, Maven |
| [Phase 9 — Go Public](./phase9-public/) | Expose to the internet with HTTPS | DDNS, Let's Encrypt, Nginx |

---

## 🖥️ Hardware

| Device | Role | Quantity |
|--------|------|----------|
| Raspberry Pi 5 | Web server (Pi #1) | 1 |
| Raspberry Pi 4 | Database server (Pi #2) | 1 |
| Raspberry Pi 4/5 | Spares / future nodes | TBD |
| Raspberry Pi Zero / Zero W | Lightweight secondary nodes | TBD |
| Raspberry Pi Pico / Pico W | Sensor collectors | TBD |
| SSD (USB) | Persistent storage for PostgreSQL | 1 |

> Hardware list will be updated once full inventory is confirmed.

---

## 🚀 Getting Started

### Prerequisites
- Raspberry Pi OS (64-bit recommended for Pi 4/5) flashed on each Pi
- Both Pi #1 and Pi #2 connected to the same local network
- SSH enabled on both Pis
- VS Code with the Claude Code extension installed on your dev machine

### Clone the Repo
```bash
git clone https://github.com/mhood76/home-pi-forge.git
cd home-pi-forge
```

### Environment Variables
Each phase that requires secrets (database passwords, API keys, etc.) uses a `.env` file. A `.env.example` is provided in each phase folder. **Never commit your `.env` files.**

```bash
cp phase4-api/.env.example phase4-api/.env
# Then fill in your values
```

---

## 📁 Project Structure

```
home-pi-forge/
├── README.md
├── .gitignore
├── LICENSE
├── docs/
│   └── architecture.md        # Detailed architecture notes
├── phase1-webserver/
│   └── README.md              # Phase-specific setup instructions
├── phase2-database/
├── phase3-data-collector/
├── phase4-api/
├── phase5-dashboard/
├── phase6-multi-device/
├── phase7-auth/
├── phase8-java-service/
└── phase9-public/
```

Each phase folder contains its own `README.md` with step-by-step setup instructions, all code for that phase, and a `.env.example` where applicable.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Server | Nginx |
| Backend API | Node.js + Express |
| Data Collection | Python 3 |
| Microservice | Java + Spring Boot |
| Database | PostgreSQL |
| Sensor Firmware | MicroPython (Pi Pico) |
| Frontend | Vanilla JavaScript + Chart.js |
| Auth | JWT + bcrypt |
| Process Manager | PM2 |
| SSL | Let's Encrypt + Certbot |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

## 🙋 Author

Built from scratch as a home lab learning project. Follow along as each phase gets added.
