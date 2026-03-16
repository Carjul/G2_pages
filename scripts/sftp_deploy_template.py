#!/usr/bin/env python3
"""
Deploy a local template directory to remote public_html via SFTP for a single domain
using credentials in ssh sftp.txt. It will backup remote files before overwriting.

Usage:
  python scripts/sftp_deploy_template.py --hosts "ssh sftp.txt" --domain bestbrokerworld.com --local G2_Site_Template0

This will upload all files under the local directory preserving relative paths under remote
public_html/. It creates remote backups by renaming existing files to <name>.pre_deploy_<ts>.bak
"""

import argparse, os, time
try:
    import paramiko
except Exception:
    print('Missing paramiko. Install: pip install paramiko')
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


def ensure_remote_dir(sftp, remote_dir):
    # create remote directory tree if needed
    dirs = []
    while remote_dir not in ('', '/'):
        dirs.append(remote_dir)
        remote_dir, _ = os.path.split(remote_dir)
    dirs = list(reversed(dirs))
    for d in dirs:
        try:
            sftp.stat(d)
        except IOError:
            try:
                sftp.mkdir(d)
            except Exception:
                pass


def deploy(local_dir, sftp, remote_base='public_html'):
    ts = time.strftime('%Y%m%d%H%M%S')
    for root, dirs, files in os.walk(local_dir):
        for fn in files:
            local_path = os.path.join(root, fn)
            rel = os.path.relpath(local_path, local_dir).replace('\\','/')
            remote_path = remote_base + '/' + rel
            remote_dir = os.path.dirname(remote_path)
            ensure_remote_dir(sftp, remote_dir)
            # backup remote if exists
            try:
                sftp.stat(remote_path)
                backup = remote_path + f'.pre_deploy_{ts}.bak'
                try:
                    sftp.rename(remote_path, backup)
                    print('  backed up', remote_path, '->', backup)
                except Exception as e:
                    print('  backup rename failed for', remote_path, e)
            except IOError:
                pass
            # upload
            try:
                sftp.put(local_path, remote_path)
                print('  uploaded', rel, '->', remote_path)
            except Exception as e:
                print('  upload failed for', local_path, e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hosts', required=True)
    ap.add_argument('--domain', required=True)
    ap.add_argument('--local', required=True)
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

    if not os.path.isdir(args.local):
        print('Local directory not found:', args.local); return

    try:
        t, sftp = sftp_connect(host, user, passwd)
    except Exception as e:
        print('SFTP connect failed:', e); return

    try:
        deploy(args.local, sftp, remote_base='public_html')
    finally:
        sftp.close(); t.close()

if __name__ == '__main__':
    main()
