#!/usr/bin/env python3
"""
Remove the tokens 'unsafe-inline' and 'unsafe-eval' from remote public_html/.htaccess
for all sites listed in 'ssh sftp.txt'. Creates a backup '.htaccess.bak' before writing.

Usage: python scripts/remove_unsafe_from_htaccess.py
"""
from pathlib import Path
import paramiko
import tempfile
import os
import sys
import re


def parse_creds_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Credentials file not found: {path}")
    entries = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split('|')]
        data = {}
        data['key'] = parts[0]
        for p in parts[1:]:
            if '=' in p:
                k, v = p.split('=', 1)
                data[k.strip()] = v.strip()
        entries.append(data)
    return entries


def process_site(entry):
    host = entry.get('host')
    user = entry.get('user')
    password = entry.get('pass')
    port = int(entry.get('port', 22))
    label = entry.get('key') or host
    if not (host and user and password):
        return (label, False, 'missing host/user/pass')

    remote_dir = 'public_html'
    remote_ht = remote_dir + '/.htaccess'
    remote_bak = remote_dir + '/.htaccess.bak'

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        return (label, False, f'sftp connect failed: {e}')

    try:
        # check existence
        try:
            sftp.stat(remote_ht)
        except IOError:
            sftp.close(); transport.close()
            return (label, False, '.htaccess not found')

        # download original to temp
        with tempfile.NamedTemporaryFile(delete=False) as tmpf:
            tmpname = tmpf.name
        try:
            sftp.get(remote_ht, tmpname)
        except Exception as e:
            sftp.close(); transport.close()
            return (label, False, f'failed to download .htaccess: {e}')

        # create remote backup
        try:
            sftp.put(tmpname, remote_bak)
        except Exception as e:
            # continue but warn
            print(f'[{label}] warning: could not create remote backup: {e}')

        # read content
        with open(tmpname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # remove occurrences of 'unsafe-inline' and 'unsafe-eval'
        new_content = re.sub(r"'unsafe-inline'", '', content)
        new_content = re.sub(r"'unsafe-eval'", '', new_content)

        # also collapse multiple spaces and duplicate semicolons optionally
        new_content = re.sub(r"\s{2,}", ' ', new_content)
        # write modified to temp and upload
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmpw:
            tmpw.write(new_content)
            tmpwname = tmpw.name

        sftp.put(tmpwname, remote_ht)
        # cleanup
        try:
            os.remove(tmpname)
        except Exception:
            pass
        try:
            os.remove(tmpwname)
        except Exception:
            pass

        sftp.close(); transport.close()
        return (label, True, 'updated')
    except Exception as e:
        try:
            sftp.close(); transport.close()
        except Exception:
            pass
        return (label, False, f'error: {e}')


def main():
    creds_path = Path('ssh sftp')
    if not creds_path.exists():
        creds_path = Path('ssh sftp.txt')
    try:
        entries = parse_creds_file(creds_path)
    except Exception as e:
        print('ERROR reading credentials file:', e)
        sys.exit(1)

    results = []
    for entry in entries:
        label = entry.get('key')
        print(f'Processing: {label} ...')
        res = process_site(entry)
        results.append(res)
        status = 'OK' if res[1] else 'FAILED'
        print(f'  {label}: {status} - {res[2]}')

    print('\nSummary:')
    for r in results:
        print(f'- {r[0]}: {"OK" if r[1] else "FAILED"} ({r[2]})')


if __name__ == '__main__':
    main()
