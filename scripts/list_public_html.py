#!/usr/bin/env python3
"""
List files in public_html on the remote host for G2_Site_Template28 using credentials in 'ssh sftp'.
"""
from pathlib import Path
import paramiko
import sys

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

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        print('ERROR: could not connect:', e)
        sys.exit(4)

    try:
        print(f"Listing remote directory: {remote_dir}")
        for entry in sftp.listdir_attr(remote_dir):
            perms = entry.st_mode
            print(f"{entry.filename}  size={entry.st_size}  attrs={entry}")
    except Exception as e:
        print('ERROR listing directory:', e)
        sftp.close(); transport.close(); sys.exit(5)

    sftp.close(); transport.close()

if __name__ == '__main__':
    main()
