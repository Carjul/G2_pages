#!/usr/bin/env python3
"""
Add a script SHA256 hash to the Content-Security-Policy script-src directive
in the remote public_html/.htaccess for a single domain parsed from ssh sftp.txt.

Usage:
  python scripts/add_csp_hash.py --hosts ssh\ sftp.txt --domain choosebestbrokers.com --hash "sha256-..."

The script creates a timestamped backup public_html/.htaccess.bak.<ts> before writing.
"""

import argparse, time, re
try:
    import paramiko
except Exception:
    print('Missing dependency paramiko. Install with: pip install paramiko')
    raise


def parse_hosts_file(path):
    entries = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split('|')]
            info = {}
            for p in parts:
                if '=' in p:
                    k,v = p.split('=',1)
                    info[k.strip()] = v.strip()
            if 'domain' in info:
                entries.append(info)
    return entries


def sftp_connect(host, user, password):
    t = paramiko.Transport((host, 22))
    t.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    return t, sftp


def add_hash_to_csp(content, hash_token):
    # Find the Content-Security-Policy header line within htaccess content
    # This will try to find script-src and add the hash inside the quotes
    pattern = re.compile(r'(Header\s+set\s+Content-Security-Policy\s+"([^"]*)")', re.IGNORECASE)
    m = pattern.search(content)
    if not m:
        return None
    full = m.group(1)
    policy = m.group(2)
    # find script-src directive
    ss_pattern = re.compile(r"script-src\s+([^;]+)")
    m2 = ss_pattern.search(policy)
    if not m2:
        # no script-src found; append one after default-src
        policy = policy.strip().rstrip(';') + f"; script-src 'self' {hash_token};"
    else:
        cur = m2.group(1).strip()
        # if hash already present, do nothing
        if hash_token in cur:
            return content
        # insert hash token into the script-src list before the semicolon
        new_cur = cur + ' ' + hash_token
        policy = policy[:m2.start(1)] + new_cur + policy[m2.end(1):]

    new_header = f'Header set Content-Security-Policy "{policy}"'
    new_content = content[:m.start(1)] + new_header + content[m.end(1):]
    return new_content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hosts', required=True)
    ap.add_argument('--domain', required=True)
    ap.add_argument('--hash', required=True)
    ap.add_argument('--remote-path', default='public_html/.htaccess')
    args = ap.parse_args()

    entries = parse_hosts_file(args.hosts)
    target = None
    for e in entries:
        if e.get('domain') == args.domain:
            target = e; break
    if not target:
        print('Domain not found in hosts file:', args.domain); return

    host = target.get('host'); user = target.get('user'); passwd = target.get('pass')
    if not all([host,user,passwd]):
        print('Missing host/user/pass for domain in hosts file'); return

    try:
        t, sftp = sftp_connect(host, user, passwd)
    except Exception as e:
        print('SFTP connect failed:', e); return

    try:
        with sftp.open(args.remote_path, 'r') as rf:
            data = rf.read()
            if isinstance(data, bytes):
                content = data.decode('utf-8', errors='ignore')
            else:
                content = data
    except Exception as e:
        print('Error reading remote file:', e); sftp.close(); t.close(); return

    new_content = add_hash_to_csp(content, args.hash)
    if new_content is None:
        print('Could not find Content-Security-Policy header in', args.remote_path); sftp.close(); t.close(); return
    if new_content == content:
        print('Hash already present or no change needed.'); sftp.close(); t.close(); return

    ts = time.strftime('%Y%m%d%H%M%S')
    backup = args.remote_path + f'.bak.{ts}'
    try:
        sftp.rename(args.remote_path, backup)
        with sftp.open(args.remote_path, 'w') as wf:
            wf.write(new_content)
        print('OK: updated .htaccess; backup at', backup)
    except Exception as e:
        print('Error writing remote file:', e)
        try:
            sftp.rename(backup, args.remote_path)
        except:
            pass
    finally:
        sftp.close(); t.close()

if __name__ == '__main__':
    main()
