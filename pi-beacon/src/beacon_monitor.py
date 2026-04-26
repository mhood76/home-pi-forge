#!/usr/bin/env python3
"""
pi-beacon — Network Status Monitor
===================================
Cycles through 5 Pi devices on the local network, displaying a status card
for each on the Waveshare 2.13" e-Paper HAT V4 (250x122, B/W, SPI).

Each card shows: hostname, IP, uptime, CPU%, CPU temp, memory usage.
Unreachable devices show dashes and are marked DOWN.

Prerequisites (run once on pi-beacon before first use):
  ssh-copy-id user@pi-webserver.local   # repeat for each device
  ssh-copy-id user@pi-database.local
  ssh-copy-id user@pi-nexus.local
  ssh-copy-id user@pi-desktop.local
  ssh-copy-id user@pi-home.local
"""

import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from waveshare_epd import epd2in13_V4 as epd_module
except ImportError as e:
    print(f"[ERROR] Cannot import waveshare_epd: {e}")
    print("  Fix: sudo pip3 install waveshare-epd --break-system-packages")
    sys.exit(1)

from PIL import Image, ImageDraw, ImageFont

# ── Configuration ─────────────────────────────────────────────────────────────

SSH_USER     = "mark"
SSH_TIMEOUT  = 5    # seconds before an SSH connect attempt is abandoned
DISPLAY_SECS = 5    # seconds each status card is shown before rotating

DEVICES = [
    {"name": "pi-webserver", "host": "pi-webserver.local"},
    {"name": "pi-database",  "host": "pi-database.local"},
    {"name": "pi-nexus",     "host": "pi-nexus.local"},
    {"name": "pi-desktop",   "host": "pi-desktop.local"},
    {"name": "pi-home",      "host": "pi-home.local"},
]

# Single SSH session — prints one metric per line, in order:
#   0: hostname   1: IP   2: uptime   3: CPU%   4: temp   5: memory
_REMOTE_CMD = (
    "hostname; "
    "hostname -I | awk '{print $1}'; "
    "uptime -p | sed 's/^up //'; "
    "vmstat 1 2 | tail -1 | awk '{print 100-$15}'; "
    "vcgencmd measure_temp 2>/dev/null | sed 's/temp=//' "
        "|| awk '{printf \"%.1fC\", $1/1000}' /sys/class/thermal/thermal_zone0/temp; "
    "free -m | awk 'NR==2{printf \"%d / %d MB\", $3,$2}'"
)

_DASHES = "---"

# ── SSH metric collection ─────────────────────────────────────────────────────

def _abbrev_uptime(raw: str) -> str:
    """Shorten 'uptime -p' output (e.g. '2 days, 3 hours' → '2d 3h') to fit display."""
    s = (raw
         .replace(" weeks",   "w").replace(" week",   "w")
         .replace(" days",    "d").replace(" day",    "d")
         .replace(" hours",   "h").replace(" hour",   "h")
         .replace(" minutes", "m").replace(" minute", "m")
         .replace(", ", " "))
    return s[:20]


def collect_metrics(device: dict) -> dict:
    """SSH into one device and return its metrics. Returns DOWN state on any failure."""
    result = {
        "name":   device["name"],
        "up":     False,
        "ip":     _DASHES,
        "uptime": _DASHES,
        "cpu":    _DASHES,
        "temp":   _DASHES,
        "mem":    _DASHES,
    }
    try:
        proc = subprocess.run(
            [
                "ssh",
                "-o", f"ConnectTimeout={SSH_TIMEOUT}",
                "-o", "StrictHostKeyChecking=no",
                "-o", "BatchMode=yes",          # never prompt for a password
                f"{SSH_USER}@{device['host']}",
                _REMOTE_CMD,
            ],
            capture_output=True,
            text=True,
            timeout=SSH_TIMEOUT + 8,            # outer guard > SSH_TIMEOUT
        )
        if proc.returncode == 0:
            lines = proc.stdout.strip().splitlines()

            def line(n: int) -> str:
                return lines[n].strip() if n < len(lines) else _DASHES

            result["up"]     = True
            result["ip"]     = line(1)
            result["uptime"] = _abbrev_uptime(line(2))
            result["cpu"]    = f"{line(3)}%"
            result["temp"]   = line(4)
            result["mem"]    = line(5)
    except Exception:
        pass                                    # leave result in DOWN state
    return result


def collect_all() -> list:
    """Collect metrics for all devices in parallel. Returns list ordered by DEVICES."""
    results = [None] * len(DEVICES)
    with ThreadPoolExecutor(max_workers=len(DEVICES)) as pool:
        futures = {pool.submit(collect_metrics, dev): i for i, dev in enumerate(DEVICES)}
        for fut in as_completed(futures):
            results[futures[fut]] = fut.result()
    return results

# ── Rendering ─────────────────────────────────────────────────────────────────

def _load_font(size: int):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_card(
    metrics: dict,
    index: int,
    total: int,
    W: int,
    H: int,
    font_body,
    font_footer,
) -> Image.Image:
    """Return a grayscale Pillow Image for one device status card.

    The image is created in 'L' mode so that fill=128 labels dither to a
    visually lighter gray when the Waveshare driver converts to 1-bit.

    Layout (250×122):
      y=0–20   black header: hostname left, UP/DOWN right
      y=24     IP row
      y=40     Uptime row
      y=55     divider line
      y=59     CPU + Temp row (two columns)
      y=75     Mem row
      y=108–121 black footer: PiForge left, n/total right
    """
    img  = Image.new("L", (W, H), 255)
    draw = ImageDraw.Draw(img)

    # ── Header (y=0–20) ───────────────────────────────────────────────────
    draw.rectangle([(0, 0), (W - 1, 20)], fill=0)
    draw.text((4, 3), metrics["name"], font=font_body, fill=255)
    status = "UP" if metrics["up"] else "DOWN"
    sw = int(draw.textlength(status, font=font_body))
    draw.text((W - sw - 4, 3), status, font=font_body, fill=255)

    # ── Row 1: IP (y=24) ──────────────────────────────────────────────────
    draw.text((4,  24), "IP",          font=font_body, fill=128)
    draw.text((42, 24), metrics["ip"], font=font_body, fill=0)

    # ── Row 2: Uptime (y=40) ──────────────────────────────────────────────
    draw.text((4,  40), "Uptime",          font=font_body, fill=128)
    draw.text((42, 40), metrics["uptime"], font=font_body, fill=0)

    # ── Divider (y=55) ────────────────────────────────────────────────────
    draw.line([(0, 55), (W - 1, 55)], fill=0, width=1)

    # ── Row 3: CPU + Temp (y=59) ──────────────────────────────────────────
    draw.text((4,   59), "CPU",          font=font_body, fill=128)
    draw.text((42,  59), metrics["cpu"], font=font_body, fill=0)
    draw.text((110, 59), "Temp",         font=font_body, fill=128)
    draw.text((148, 59), metrics["temp"], font=font_body, fill=0)

    # ── Row 4: Mem (y=75) ─────────────────────────────────────────────────
    draw.text((4,  75), "Mem",          font=font_body, fill=128)
    draw.text((42, 75), metrics["mem"], font=font_body, fill=0)

    # ── Footer (y=108–121) ────────────────────────────────────────────────
    draw.rectangle([(0, 108), (W - 1, H - 1)], fill=0)
    draw.text((4, 111), "PiForge", font=font_footer, fill=255)
    page = f"{index + 1} / {total}"
    pw = int(draw.textlength(page, font=font_footer))
    draw.text((W - pw - 4, 111), page, font=font_footer, fill=255)

    return img.rotate(90, expand=True)

# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*52}")
    print(f"  pi-beacon  Network Monitor")
    print(f"  Devices : {', '.join(d['name'] for d in DEVICES)}")
    print(f"  Rotation: every {DISPLAY_SECS}s")
    print(f"{'='*52}\n")

    epd         = epd_module.EPD()
    W, H        = epd.height, epd.width
    font_body   = _load_font(12)
    font_footer = _load_font(10)

    print("[INIT] Starting display (full clear)...")
    epd.init()
    epd.Clear(0xFF)

    cycle = 0
    try:
        while True:
            print(f"\n[Cycle {cycle + 1}] Collecting metrics...")
            all_metrics = collect_all()
            for m in all_metrics:
                print(f"  {'UP  ' if m['up'] else 'DOWN'}  {m['name']}")

            for idx, metrics in enumerate(all_metrics):
                img = render_card(metrics, idx, len(DEVICES), W, H, font_body, font_footer)
                buf = epd.getbuffer(img)

                # V4 partial-refresh pattern: init() + display() for the first card,
                # then set it as the base image; subsequent cards call displayPartial()
                # directly (no mode-switch needed, faster waveform, no full-panel flash).
                # Full refresh every cycle prevents ghosting from accumulating.
                if idx == 0:
                    epd.init()
                    epd.display(buf)
                    epd.displayPartBaseImage(buf)
                else:
                    epd.displayPartial(buf)

                time.sleep(DISPLAY_SECS)

            cycle += 1

    except KeyboardInterrupt:
        print("\n[STOP] Interrupted — clearing display and entering sleep mode.")
        epd.init()
        epd.Clear(0xFF)
        epd.sleep()
        print("[DONE] Display is in low-power sleep mode.")


if __name__ == "__main__":
    main()
