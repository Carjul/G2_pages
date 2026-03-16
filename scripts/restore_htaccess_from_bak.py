#!/usr/bin/env python3
"""
Restore remote public_html/.htaccess from public_html/.htaccess.bak for all sites
listed in 'ssh sftp' or 'ssh sftp.txt'. Before restoring, save the current .htaccess as
`.htaccess.pre_restore_<timestamp>.bak` so you can rollback again if needed.

Usage: python scripts/restore_htaccess_from_bak.py
"""
from pathlib import Path
import paramiko
import tempfile
import os
import sys
import time


def parse_creds_file(path: Path):
    text = path.read_text(encoding='utf-8')
    entries = []
    for line in text.splitlines():
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


def restore_site(entry):
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
        # check that backup exists
        try:
            sftp.stat(remote_bak)
        except IOError:
            sftp.close(); transport.close()
            return (label, False, '.htaccess.bak not found')

        timestamp = time.strftime('%Y%m%d%H%M%S')
        remote_pre = remote_dir + f'/.htaccess.pre_restore_{timestamp}.bak'

        # if .htaccess exists, move it to pre_restore
        try:
            sftp.stat(remote_ht)
            try:
                sftp.rename(remote_ht, remote_pre)
                pre_note = f'moved existing .htaccess to {remote_pre}'
            except Exception:
                # fallback: download then upload as remote_pre
                with tempfile.NamedTemporaryFile(delete=False) as tmpf:
                    tmpname = tmpf.name
                sftp.get(remote_ht, tmpname)
                sftp.put(tmpname, remote_pre)
                try:
                    os.remove(tmpname)
                except Exception:
                    pass
                pre_note = f'copied existing .htaccess to {remote_pre}'
        except IOError:
            pre_note = 'no existing .htaccess'

        # now restore: try rename .bak -> .htaccess
        try:
            sftp.rename(remote_bak, remote_ht)
            action_note = 'renamed .htaccess.bak -> .htaccess'
        except Exception:
            # fallback: download bak and upload as .htaccess
            with tempfile.NamedTemporaryFile(delete=False) as tmpf2:
                tmpbak = tmpf2.name
            sftp.get(remote_bak, tmpbak)
            sftp.put(tmpbak, remote_ht)
            try:
                os.remove(tmpbak)
            except Exception:
                pass
            action_note = 'copied .htaccess.bak content to .htaccess'

        sftp.close(); transport.close()
        return (label, True, f'{pre_note}; {action_note}')
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
        print(f'Processing restore: {label} ...')
        res = restore_site(entry)
        results.append(res)
        status = 'OK' if res[1] else 'FAILED'
        print(f'  {label}: {status} - {res[2]}')

    print('\nSummary:')
    for r in results:
        print(f'- {r[0]}: {"OK" if r[1] else "FAILED"} ({r[2]})')


if __name__ == '__main__':
    main()
