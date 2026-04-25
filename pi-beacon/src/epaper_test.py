#!/usr/bin/env python3
"""
pi-beacon — Waveshare 2.13" e-Paper HAT Test
=============================================
Tests the display with progressively complex output:
  1. Full clear (white)
  2. Hello World text
  3. Simple shapes + hostname/IP info
  4. Partial refresh test (if supported by your variant)

Supports: epd2in13 / V2 / V3 / V4
Run with: python3 epaper_test.py [--variant V4]
"""

import sys
import time
import argparse
import socket
import subprocess

# ── Argument parsing ──────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Waveshare 2.13\" e-Paper test")
parser.add_argument(
    "--variant",
    choices=["V1", "V2", "V3", "V4"],
    default="V4",
    help="Display variant (default: V4). Check the sticker on the back of your HAT.",
)
parser.add_argument(
    "--no-clear",
    action="store_true",
    help="Skip the initial full clear (faster during dev)",
)
args = parser.parse_args()

# ── Import the correct driver ─────────────────────────────────────────────────
try:
    from waveshare_epd import epd2in13_V4 as epd_module
    if args.variant == "V1":
        from waveshare_epd import epd2in13 as epd_module
    elif args.variant == "V2":
        from waveshare_epd import epd2in13_V2 as epd_module
    elif args.variant == "V3":
        from waveshare_epd import epd2in13_V3 as epd_module
    print(f"[OK] Loaded driver: epd2in13 variant {args.variant}")
except ImportError as e:
    print(f"[ERROR] Could not import waveshare_epd: {e}")
    print()
    print("  Fix: install the Waveshare library:")
    print("    pip3 install waveshare-epd --break-system-packages")
    sys.exit(1)

from PIL import Image, ImageDraw, ImageFont

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_hostname():
    return socket.gethostname()

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No IP"

def get_temp():
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"],
            capture_output=True, text=True, timeout=3
        )
        return result.stdout.strip().replace("temp=", "")
    except Exception:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                millideg = int(f.read().strip())
                return f"{millideg / 1000:.1f}°C"
        except Exception:
            return "N/A"

def load_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*48}")
    print(f"  pi-beacon  e-Paper Test  ({args.variant})")
    print(f"{'='*48}")

    epd = epd_module.EPD()
    W, H = epd.width, epd.height
    print(f"[INFO] Display size: {W}×{H}")

    # ── Step 1: Init + clear ──────────────────────────────────────────────
    print("[1/4] Initialising display...")
    epd.init()

    if not args.no_clear:
        print("      Clearing display (full refresh)...")
        epd.Clear(0xFF)
        time.sleep(1)

    font_lg = load_font(20)
    font_md = load_font(14)
    font_sm = load_font(11)

    # ── Step 2: Hello World ───────────────────────────────────────────────
    print("[2/4] Drawing Hello World...")
    img = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W-1, H-1)], outline=0, width=2)
    draw.text((10, 10),  "Hello World!",   font=font_lg, fill=0)
    draw.text((10, 38),  "pi-beacon",      font=font_md, fill=0)
    draw.text((10, 58),  "e-Paper HAT OK", font=font_sm, fill=0)
    draw.line([(10, 76), (W-10, 76)], fill=0, width=1)
    draw.text((10, 82), "Waveshare 2.13\"", font=font_sm, fill=0)

    epd.display(epd.getbuffer(img))
    time.sleep(3)

    # ── Step 3: System info ───────────────────────────────────────────────
    print("[3/4] Drawing system info...")
    hostname = get_hostname()
    ip       = get_ip()
    temp     = get_temp()

    img2 = Image.new("1", (W, H), 255)
    draw2 = ImageDraw.Draw(img2)

    draw2.rectangle([(0, 0), (W, 20)], fill=0)
    draw2.text((4, 2), f" {hostname}", font=font_md, fill=255)

    rows = [
        ("IP  :", ip),
        ("Temp:", temp),
        ("Disp:", f"2.13\" ePaper {args.variant}"),
        ("SPI :", "enabled"),
    ]
    y = 26
    for label, value in rows:
        draw2.text((4,  y), label, font=font_sm, fill=0)
        draw2.text((42, y), value, font=font_sm, fill=0)
        y += 18

    draw2.line([(0, H-14), (W, H-14)], fill=0, width=1)
    draw2.text((4, H-13), "PiForge  home-pi-forge", font=font_sm, fill=0)

    epd.display(epd.getbuffer(img2))
    time.sleep(4)

    # ── Step 4: Partial refresh ───────────────────────────────────────────
    print("[4/4] Partial refresh test...")
    try:
        epd.init(epd.PART_UPDATE)

        for i in range(5):
            temp = get_temp()
            img3 = Image.new("1", (W, H), 255)
            draw3 = ImageDraw.Draw(img3)

            draw3.rectangle([(0, 0), (W, 20)], fill=0)
            draw3.text((4, 2), f" {hostname}", font=font_md, fill=255)

            rows = [
                ("IP  :", ip),
                ("Temp:", temp),
                ("Disp:", f"2.13\" ePaper {args.variant}"),
                ("SPI :", "enabled"),
            ]
            y = 26
            for label, value in rows:
                draw3.text((4,  y), label, font=font_sm, fill=0)
                draw3.text((42, y), value, font=font_sm, fill=0)
                y += 18

            draw3.line([(0, H-14), (W, H-14)], fill=0, width=1)
            draw3.text((4, H-13), f"PiForge  refresh #{i+1}/5", font=font_sm, fill=0)

            epd.displayPartial(epd.getbuffer(img3))
            print(f"      Partial refresh {i+1}/5 — Temp: {temp}")
            time.sleep(2)

    except AttributeError:
        print("      (Partial refresh not available on this variant — skipping)")

    # ── Done ──────────────────────────────────────────────────────────────
    print("\n[OK] Test complete. Putting display to sleep.")
    epd.sleep()
    print("     Display is now in low-power sleep mode.\n")


if __name__ == "__main__":
    main()
