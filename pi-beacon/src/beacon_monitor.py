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
    "free -m | awk 'NR==2{printf \"%dMB/%dMB (%.0f%%)\", $3,$2,100*$3/$2}'"
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
    font_md,
    font_sm,
) -> Image.Image:
    """Return a 1-bit Pillow Image for one device status card.

    Layout (250×122):
      0–17   black header: device name left, UP/DOWN right
      23–68  four metric rows (IP, Up, CPU+Temp, Mem)
      101    separator line
      101–121 footer: dot indicators left, project name right
    """
    img  = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(img)

    # ── Header bar ────────────────────────────────────────────────────────
    HDR = 18
    draw.rectangle([(0, 0), (W - 1, HDR - 1)], fill=0)
    draw.text((4, 2), metrics["name"], font=font_md, fill=255)

    status = "UP" if metrics["up"] else "DOWN"
    sw = int(draw.textlength(status, font=font_md))
    draw.text((W - sw - 4, 2), status, font=font_md, fill=255)

    # ── Metric rows ───────────────────────────────────────────────────────
    LX  = 4    # label column x
    VX  = 46   # value column x
    LX2 = 132  # second-label column x (for CPU+Temp row)
    VX2 = 172  # second-value column x
    y   = HDR + 5

    def metric_row(label, value, label2=None, value2=None):
        nonlocal y
        draw.text((LX, y), label, font=font_sm, fill=0)
        draw.text((VX, y), value, font=font_sm, fill=0)
        if label2 is not None:
            draw.text((LX2, y), label2, font=font_sm, fill=0)
            draw.text((VX2, y), value2, font=font_sm, fill=0)
        y += 15

    metric_row("IP",  metrics["ip"])
    metric_row("Up",  metrics["uptime"])
    metric_row("CPU", metrics["cpu"], "Temp", metrics["temp"])
    metric_row("Mem", metrics["mem"])

    # ── Footer ────────────────────────────────────────────────────────────
    SEP_Y  = H - 21    # 101 — separator line
    DOT_CY = H - 9     # 113 — dot vertical centre
    DOT_R  = 3
    TEXT_Y = DOT_CY - 7  # 106 — top of footer text, vertically centred with dots

    draw.line([(0, SEP_Y), (W - 1, SEP_Y)], fill=0, width=1)

    # Filled dot = current device; outline dot = other devices
    for i in range(total):
        cx = 6 + i * (DOT_R * 2 + 5)
        bb = [(cx - DOT_R, DOT_CY - DOT_R), (cx + DOT_R, DOT_CY + DOT_R)]
        if i == index:
            draw.ellipse(bb, fill=0)
        else:
            draw.ellipse(bb, outline=0)

    label = "home-pi-forge"
    lw = int(draw.textlength(label, font=font_sm))
    draw.text((W - lw - 4, TEXT_Y), label, font=font_sm, fill=0)

    return img

# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*52}")
    print(f"  pi-beacon  Network Monitor")
    print(f"  Devices : {', '.join(d['name'] for d in DEVICES)}")
    print(f"  Rotation: every {DISPLAY_SECS}s")
    print(f"{'='*52}\n")

    epd     = epd_module.EPD()
    W, H    = epd.width, epd.height
    font_md = _load_font(14)
    font_sm = _load_font(11)

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
                img = render_card(metrics, idx, len(DEVICES), W, H, font_md, font_sm)

                # Full refresh at the start of each cycle clears partial-refresh
                # ghosting. Cards 2-5 within a cycle use faster partial refresh.
                if idx == 0:
                    epd.init()
                    epd.display(epd.getbuffer(img))
                else:
                    epd.init_part()
                    epd.displayPartial(epd.getbuffer(img))

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
