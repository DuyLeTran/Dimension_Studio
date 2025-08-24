#!/usr/bin/env python3
"""
deploy.py - chạy Django + Cloudflared tunnel để public tạm thời

Usage:
    python deploy.py
"""

import os
import subprocess
import sys
import time
import signal

PORT = 8000
TUNNEL_BIN = "cloudflared"   # đảm bảo đã cài cloudflared và nằm trong PATH

def main():
    # B1: chạy Django server ở 0.0.0.0:8000
    print(f"[INFO] Starting Django server on 0.0.0.0:{PORT} ...")
    django_proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", f"0.0.0.0:{PORT}"],
        stdout=sys.stdout, stderr=sys.stderr
    )
    time.sleep(3)  # chờ Django khởi động

    # B2: chạy cloudflared tunnel
    print("[INFO] Starting Cloudflared tunnel...")
    tunnel_proc = subprocess.Popen(
        [TUNNEL_BIN, "tunnel", "--url", f"http://localhost:{PORT}"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    try:
        # In ra log cloudflared để lấy URL public
        for line in tunnel_proc.stdout:
            print(line, end="")
            # Cloudflared sẽ in ra URL dạng https://xxxx.trycloudflare.com
    except KeyboardInterrupt:
        print("\n[INFO] Stopping...")

    # B3: nếu Ctrl+C thì dừng cả 2 process
    finally:
        tunnel_proc.terminate()
        django_proc.terminate()
        try:
            tunnel_proc.wait(timeout=5)
            django_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tunnel_proc.kill()
            django_proc.kill()
        print("[INFO] Stopped Django & Cloudflared.")

if __name__ == "__main__":
    main()