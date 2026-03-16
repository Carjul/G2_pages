#!/usr/bin/env python3
"""
Open each domain from a hosts file in the system browser and run a quick HTTP check.

Usage:
  python scripts/check_and_open_sites.py --hosts "ssh sftp.txt" [--no-open] [--output report.csv]

The script parses lines like those in `ssh sftp.txt` (domain=example.com | host=... | user=...)
and attempts an HTTPS request to each `domain`. By default it also opens each URL in the
default system browser (one tab per site). Results are printed and saved to CSV.
"""

import argparse
import csv
import re
import sys
import time
import webbrowser

try:
    import requests
except Exception:
    print('Missing dependency "requests". Install with: pip install requests')
    raise


def parse_hosts_file(path):
    domains = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split('|')]
            info = {}
            for p in parts:
                if '=' in p:
                    k, v = p.split('=', 1)
                    info[k.strip()] = v.strip()
            # fallback: try to extract a bare token that looks like a domain
            domain = info.get('domain')
            if not domain:
                # try to find token that contains a dot
                tokens = [t for t in re.split(r'[\s|]+', line) if '.' in t]
                if tokens:
                    domain = tokens[0].strip()
            if domain:
                domains.append(domain)
    return domains


def fetch_info(url, timeout=10):
    try:
        t0 = time.time()
        resp = requests.get(url, timeout=timeout, allow_redirects=True)
        elapsed = time.time() - t0
        content = resp.text or ''
        m = re.search(r'<title\b[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = m.group(1).strip() if m else ''
        return {
            'status_code': resp.status_code,
            'reason': resp.reason,
            'content_type': resp.headers.get('Content-Type',''),
            'content_length': len(content),
            'title': title.replace('\n',' ').replace('\r',' ').strip(),
            'elapsed_s': round(elapsed, 3),
        }
    except requests.RequestException as e:
        return {'error': str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hosts', default='ssh sftp.txt', help='hosts file to parse (default: ssh sftp.txt)')
    ap.add_argument('--no-open', action='store_true', help="Don't open URLs in the system browser")
    ap.add_argument('--output', default='site_check_report.csv', help='CSV output file')
    args = ap.parse_args()

    try:
        domains = parse_hosts_file(args.hosts)
    except FileNotFoundError:
        print('Hosts file not found:', args.hosts, file=sys.stderr)
        sys.exit(2)

    if not domains:
        print('No domains found in', args.hosts)
        sys.exit(0)

    print(f'Found {len(domains)} domains; opening in browser: {not args.no_open}')

    rows = []
    for d in domains:
        url = f'https://{d}'
        print(f'Checking {url} ...', end=' ', flush=True)
        info = fetch_info(url)
        ok = False
        if 'error' in info:
            print('ERROR ->', info['error'])
        else:
            ok = 200 <= info['status_code'] < 400
            print(f'{info["status_code"]} {info.get("reason","")}', end='')
        if info.get('title'):
            # sanitize title for console encoding (avoid UnicodeEncodeError on Windows consoles)
            enc = sys.stdout.encoding or 'utf-8'
            safe_title = info['title'][:80].encode(enc, errors='replace').decode(enc)
            print(' -', safe_title, end='')
            print()

        rows.append({
            'domain': d,
            'url': url,
            'ok': ok,
            **({k: info.get(k) for k in ('status_code','reason','content_type','content_length','title','elapsed_s')} if 'error' not in info else {'error': info['error']})
        })

        if not args.no_open:
            # open in a new browser tab
            try:
                webbrowser.open_new_tab(url)
            except Exception:
                pass

    # write CSV
    fieldnames = ['domain','url','ok','status_code','reason','content_type','content_length','title','elapsed_s','error']
    with open(args.output, 'w', newline='', encoding='utf-8') as csvf:
        w = csv.DictWriter(csvf, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            row = {k: r.get(k, '') for k in fieldnames}
            w.writerow(row)

    print('\nReport saved to', args.output)


if __name__ == '__main__':
    main()
