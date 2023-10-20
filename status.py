#!/usr/bin/python3

# 1. install this program as ~/.config/sway/status.py
# 
# 2. add sway-bar(5) section in ~/.config/sway/config
#
# bar {
#     position top
# 
#     status_command ~/.config/sway/status.py
# 
#     colors {
#         statusline #ffffff
#         background #323232
#         inactive_workspace #32323200 #32323200 #5c5c5c
#     }
#     font pango:DejaVu Sans Mono 10
# }
#
# 3. run `swaymsg reload`

from datetime import datetime
from psutil import disk_usage, sensors_battery
from psutil._common import bytes2human
from socket import gethostname, gethostbyname
from subprocess import check_output
from sys import stdout
from time import sleep

import socket
import subprocess

def ip():
   # creates a temporary socket to quad9.net
   # to IPv4 and IPv6 addresses to retrieve
   # own IP address, no connection is made
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      s.connect(('9.9.9.9', 1))
    except OSError:
      return ""
    return s.getsockname()[0]

def ip6():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
      s.connect(('2620:fe::fe', 1))
    except OSError:
      return ""
    return s.getsockname()[0]

def write(data):
    stdout.write('%s\n' % data)
    stdout.flush()

def ssid():
    # uses `iwgetid` from `wireless-tools` to retrieve SSID
    try:
        return check_output("iwgetid -r", shell=True).strip().decode("utf-8")
    except Exception:
        return ""

def signal():
    with open("/proc/net/wireless") as f:
      for line in f.readlines():
        a = line.split(" ")
        if ':' in a[0]:
          s = round(100*int(a[4].strip('.'))/70)
          return f"{s}%"
    return ""
    
def refresh():
    disk = bytes2human(disk_usage('/').free)
    battery = int(sensors_battery().percent)
    if battery < 15:
      low = "⚠️"
      subprocess.Popen(['/usr/bin/swaynag','-m','⚠️Battery low'])
    elif battery < 10:
      low = "⚠️⚠️"
    elif battery < 5:
      low = "⚠️⚠️⚠️"
    else:
      low = ""
    status = "🔌" if sensors_battery().power_plugged else "🔋"
    date = datetime.now().strftime('%H:%M %a %d %b')
    write(f'{ip()} {ip6()} {ssid()} {signal()} | 📂 {disk} | ⚡ {battery}% <b>{low}</b> {status} | {date}')

while True:
    refresh()
    sleep(1)
