#!/usr/bin/env python3
"""
Uptime tracker for urgpedia services.
Checks each service every run and writes aggregated stats to uptime.json.

Deploy:
  scp scripts/uptime-track.py ubuntu@146.235.242.103:/home/ubuntu/
  crontab -e   →  */5 * * * * python3 /home/ubuntu/uptime-track.py

Files:
  /home/ubuntu/uptime.log          — timestamped check log (auto-trimmed to 8 days)
  /srv/urgpedia/assets/uptime.json — consumed by status.js
"""

import json
import os
import subprocess
import time

LOG = '/home/ubuntu/uptime.log'
OUT = '/srv/urgpedia/assets/uptime.json'


def check_http(url):
    """Returns True if server responds with any HTTP code (not timeout/error)."""
    try:
        r = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
             '--max-time', '7', '--connect-timeout', '5', '-L', url],
            capture_output=True, text=True, timeout=10,
        )
        code = r.stdout.strip()
        return bool(code) and code != '000'
    except Exception:
        return False


now = int(time.time())

checks = {
    'urgpedia': True,                          # server is up (script is running)
    'caspm':    check_http('http://localhost:3000/'),
    'auth0':    check_http('https://dev-0zpeshonra8ull1d.us.auth0.com/'
                           '.well-known/openid-configuration'),
}

# Append results to log
with open(LOG, 'a') as f:
    for svc, up in checks.items():
        f.write(f'{now} {svc} {1 if up else 0}\n')

# Trim log to last 8 days
cutoff = now - 8 * 86400
lines_kept = []
with open(LOG) as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            try:
                if int(parts[0]) > cutoff:
                    lines_kept.append(line)
            except ValueError:
                pass

with open(LOG, 'w') as f:
    f.writelines(lines_kept)

# Compute uptime percentages (day / week)
day_start  = now - 86400
week_start = now - 7 * 86400
data = {svc: {'day': [], 'week': []} for svc in checks}

for line in lines_kept:
    parts = line.strip().split()
    if len(parts) != 3:
        continue
    try:
        ts, svc, up = int(parts[0]), parts[1], int(parts[2])
    except ValueError:
        continue
    if svc not in data:
        continue
    if ts >= day_start:
        data[svc]['day'].append(up)
    if ts >= week_start:
        data[svc]['week'].append(up)

# Compute hourly slots for the last 7 days (168 slots, index 0 = oldest)
SLOTS = 168
slot_start = now - SLOTS * 3600
hours_raw = {svc: [[] for _ in range(SLOTS)] for svc in checks}

for line in lines_kept:
    parts = line.strip().split()
    if len(parts) != 3:
        continue
    try:
        ts, svc, up = int(parts[0]), parts[1], int(parts[2])
    except ValueError:
        continue
    if svc not in hours_raw:
        continue
    if ts < slot_start:
        continue
    idx = int((ts - slot_start) // 3600)
    if 0 <= idx < SLOTS:
        hours_raw[svc][idx].append(up)

result = {'updated': now, 'services': {}}
for svc in checks:
    d = data[svc]
    h = hours_raw[svc]
    result['services'][svc] = {
        'day':  round(sum(d['day'])  / len(d['day'])  * 100, 1) if d['day']  else None,
        'week': round(sum(d['week']) / len(d['week']) * 100, 1) if d['week'] else None,
        'hours': [
            round(sum(bucket) / len(bucket), 2) if bucket else None
            for bucket in h
        ],
    }

with open(OUT, 'w') as f:
    json.dump(result, f)
