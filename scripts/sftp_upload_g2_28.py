#!/usr/bin/env python3
"""
sftp_upload_g2_28.py

Recursively upload local directory G2_Site_Template28 to remote public_html via SFTP
using credentials from local file `ssh sftp` (entry G2_Site_Template28).

WARNING: This will overwrite files on the remote with the same path/name.
"""
from pathlib import Path
import paramiko
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


def ensure_remote_dir(sftp, remote_directory):
    # Recursively ensure remote directory exists
    dirs = []
    head = remote_directory
    while head not in ('', '/'):
        dirs.append(head)
        head = os.path.dirname(head)
    dirs = list(reversed(dirs))
    for d in dirs:
        try:
            sftp.stat(d)
        except IOError:
            try:
                sftp.mkdir(d)
                print(f"Created remote dir: {d}")
            except Exception as e:
                # Could be race or permission; ignore if exists
                print(f"Could not create remote dir {d}: {e}")


def upload_dir(sftp, local_root: Path, remote_root: str):
    files_uploaded = 0
    for root, dirs, files in os.walk(local_root):
        rel = os.path.relpath(root, local_root)
        if rel == '.':
            remote_dir = remote_root
        else:
            remote_dir = os.path.join(remote_root, rel).replace('\\', '/')
        ensure_remote_dir(sftp, remote_dir)
        for fname in files:
            local_path = os.path.join(root, fname)
            # skip backup files created by script or local scripts directory
            if local_path.endswith('.bak'):
                continue
            # Optionally skip .git and scripts
            if '/.git/' in local_path or local_path.startswith('scripts'):
                continue
            remote_path = remote_dir.rstrip('/') + '/' + fname
            try:
                sftp.put(local_path, remote_path)
                files_uploaded += 1
                print(f"Uploaded {local_path} -> {remote_path}")
            except Exception as e:
                print(f"Failed to upload {local_path}: {e}")
    return files_uploaded


def main():
    # prefer plaintext creds file without extension; fallback to 'ssh sftp.txt'
    creds_file = Path('ssh sftp')
    if not creds_file.exists():
        creds_file = Path('ssh sftp.txt')
    try:
        data = parse_credentials(creds_file, 'G2_Site_Template28')
    except Exception as e:
        print('ERROR:', e)
        sys.exit(2)

    host = data.get('host')
    user = data.get('user')
    password = data.get('pass')
    port = int(data.get('port', 22))

    local_dir = Path('G2_Site_Template28')
    if not local_dir.exists():
        print('ERROR: local directory not found:', local_dir)
        sys.exit(3)

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        print('ERROR: could not connect:', e)
        sys.exit(4)

    remote_root = 'public_html'
    print(f"Uploading contents of {local_dir} to {user}@{host}:{remote_root} ...")
    count = upload_dir(sftp, local_dir, remote_root)
    print(f"Done. Files uploaded: {count}")

    sftp.close(); transport.close()


if __name__ == '__main__':
    main()
