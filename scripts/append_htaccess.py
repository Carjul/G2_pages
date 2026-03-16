#!/usr/bin/env python3
"""
append_htaccess.py

Append the contents of local file 'segurity.txt' into the remote
'.htaccess' located in 'public_html' for G2_Site_Template28 using
credentials in the local file 'ssh sftp'. Creates a remote backup
'.htaccess.bak' before modifying.
"""
from pathlib import Path
import paramiko
import tempfile
import sys
import os


def parse_credentials(file_path: Path, key_prefix: str = 'G2_Site_Template28'):
    text = file_path.read_text(encoding='utf-8')
    for line in text.splitlines():
        if line.startswith(key_prefix):
            parts = [p.strip() for p in line.split('|')]
            data = {}
            for p in parts[1:]:
                if '=' in p:
                    k, v = p.split('=', 1)
                    data[k.strip()] = v.strip()
            return data
    raise ValueError(f"No entry for {key_prefix} found in {file_path}")


def main():
    creds_file = Path('ssh sftp')
    sec_file = Path('segurity.txt')
    if not sec_file.exists():
        print('ERROR: local segurity.txt not found')
        sys.exit(2)

    try:
        data = parse_credentials(creds_file, 'G2_Site_Template28')
    except Exception as e:
        print('ERROR reading credentials:', e)
        sys.exit(3)

    host = data.get('host')
    user = data.get('user')
    password = data.get('pass')
    port = int(data.get('port', 22))

    if not (host and user and password):
        print('ERROR: missing host/user/password in credentials')
        sys.exit(4)

    remote_dir = 'public_html'
    remote_ht = remote_dir + '/.htaccess'
    remote_bak = remote_dir + '/.htaccess.bak'

    # read local segurity content
    sec_text = sec_file.read_text(encoding='utf-8')

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        print('ERROR: could not connect via SFTP:', e)
        sys.exit(5)

    # create backup if .htaccess exists
    try:
        sftp.stat(remote_ht)
        # download then upload as backup (ensures permission/ownership preserved as new file)
        with tempfile.NamedTemporaryFile(delete=False) as tmpf:
            tmpname = tmpf.name
        try:
            sftp.get(remote_ht, tmpname)
            sftp.put(tmpname, remote_bak)
            print(f'Created remote backup: {remote_bak}')
        finally:
            try:
                os.remove(tmpname)
            except Exception:
                pass
    except IOError:
        # no existing .htaccess — we'll create one
        print('No existing .htaccess found; will create new one.')

    # prepare new content: append segury text to existing content (if any)
    new_content = ''
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmpf:
            # if remote exists, fetch its content first
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmpget:
                    tmpgetname = tmpget.name
                sftp.get(remote_ht, tmpgetname)
                with open(tmpgetname, 'r', encoding='utf-8') as r:
                    existing = r.read()
                os.remove(tmpgetname)
            except Exception:
                existing = ''
            combined = existing + '\n' + sec_text
            tmpf.write(combined)
            tmpfname = tmpf.name
        # upload combined file
        sftp.put(tmpfname, remote_ht)
        print(f'Appended segurity.txt to {remote_ht}')
    except Exception as e:
        print('ERROR while writing remote .htaccess:', e)
        sftp.close(); transport.close(); sys.exit(6)
    finally:
        try:
            os.remove(tmpfname)
        except Exception:
            pass

    sftp.close(); transport.close()
    print('Done.')


if __name__ == '__main__':
    main()
