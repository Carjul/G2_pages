#!/usr/bin/env python3
"""
rename_remote.py

Reads credentials for G2_Site_Template28 from the local file 'ssh sftp'
and performs an SFTP rename of public_html/index.php -> public_html/index.php22

This script uses paramiko. It avoids printing sensitive data.
"""
from pathlib import Path
import paramiko
import sys
import re


def parse_credentials(file_path: Path, key_prefix: str = 'G2_Site_Template28'):
    if not file_path.exists():
        raise FileNotFoundError(f"credentials file not found: {file_path}")
    text = file_path.read_text(encoding='utf-8')
    for line in text.splitlines():
        if line.startswith(key_prefix):
            # example line format: G2_Site_Template28 | domain=nextgeeninvesting.com | host=161.35.220.176 | user=nextgeeninvesting | pass=bxy_gdb0rdy7XGN2nmx
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
    try:
        data = parse_credentials(creds_file, 'G2_Site_Template28')
    except Exception as e:
        print('ERROR:', e)
        sys.exit(2)

    host = data.get('host')
    user = data.get('user')
    password = data.get('pass')
    port = int(data.get('port', 22))

    if not (host and user and password):
        print('ERROR: missing host/user/password in credentials')
        sys.exit(3)

    remote_dir = 'public_html'
    src = 'index.php'
    dst = 'index.php22'

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        print('ERROR: could not connect:', e)
        sys.exit(4)

    remote_src = f"{remote_dir}/{src}"
    remote_dst = f"{remote_dir}/{dst}"

    try:
        # verify source exists
        sftp.stat(remote_src)
    except Exception as e:
        print(f'ERROR: remote source not found: {remote_src} ({e})')
        sftp.close(); transport.close()
        sys.exit(5)

    try:
        sftp.rename(remote_src, remote_dst)
        print(f"OK: Renamed {remote_src} -> {remote_dst}")
    except Exception as e:
        print('ERROR: rename failed:', e)
        sftp.close(); transport.close()
        sys.exit(6)

    sftp.close(); transport.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
