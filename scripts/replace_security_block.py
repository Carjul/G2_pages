#!/usr/bin/env python3
# Replace the security block in remote public_html/.htaccess on multiple hosts
# Usage: python scripts/replace_security_block.py --hosts hosts.txt --security security.txt [--dry-run]

import argparse, os, time, difflib
try:
    import paramiko
except Exception as e:
    print('Missing dependency paramiko. Install with: pip install paramiko')
    raise

def parse_hosts_file(path):
    hosts = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split('|')]
            info = {}
            if any('=' in p for p in parts):
                for p in parts:
                    if '=' in p:
                        k,v = p.split('=',1)
                        info[k.strip()] = v.strip()
                    else:
                        if 'id' not in info:
                            info['id'] = p
            else:
                tokens = line.split()
                if '@' in tokens[0]:
                    user, host = tokens[0].split('@',1)
                    info['host'] = host; info['user'] = user
                elif len(tokens) >= 2:
                    info['host'] = tokens[0]; info['user'] = tokens[1]
                else:
                    continue
            hosts.append({
                'id': info.get('id') or info.get('domain') or info.get('host'),
                'domain': info.get('domain'),
                'host': info.get('host'),
                'user': info.get('user'),
                'pass': info.get('pass'),
            })
    return hosts

def sftp_connect(host, user, password):
    t = paramiko.Transport((host, 22))
    t.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    return t, sftp

def replace_block(content, replacement):
    start_marker = 'SEGURIDAD: Implementación de Security Headers'
    idx = content.find(start_marker)
    if idx == -1:
        # marker not found -> append replacement at end
        return content.rstrip() + '\n\n' + replacement + '\n', True
    start_line_idx = content.rfind('\n', 0, idx) + 1
    end_tag = '</IfModule>'
    end_idx = content.find(end_tag, idx)
    if end_idx == -1:
        double_nl = content.find('\n\n', idx)
        if double_nl == -1:
            end_idx = len(content)
        else:
            end_idx = double_nl
    else:
        # include the whole line with </IfModule>
        end_idx = content.find('\n', end_idx)
        if end_idx == -1:
            end_idx = len(content)
    new_content = content[:start_line_idx] + replacement + '\n' + content[end_idx:]
    return new_content, True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hosts', required=True, help='archivo con hosts (ssh sftp.txt)')
    ap.add_argument('--security', required=True, help='archivo security.txt con bloque a insertar')
    ap.add_argument('--remote-path', default='public_html/.htaccess', help='ruta remota a .htaccess')
    ap.add_argument('--dry-run', action='store_true', help='no sube archivos, solo muestra diff local')
    args = ap.parse_args()

    with open(args.security, encoding='utf-8') as f:
        replacement = f.read().strip()

    hosts = parse_hosts_file(args.hosts)
    if not hosts:
        print('No se encontraron entries válidas en', args.hosts); return

    for h in hosts:
        id_ = h.get('id') or h.get('host')
        host = h.get('host'); user = h.get('user'); passwd = h.get('pass')
        print(f'--- Procesando: {id_} ({host}) ---')
        if not all([host,user,passwd]):
            print('  SKIP: falta host/user/pass en la fila (no intento conectar).')
            continue
        try:
            t, sftp = sftp_connect(host, user, passwd)
        except Exception as e:
            print('  ERROR: conexión SFTP falló:', e); continue

        try:
            with sftp.open(args.remote_path, 'r') as rf:
                remote_bytes = rf.read()
                if isinstance(remote_bytes, bytes):
                    remote_content = remote_bytes.decode('utf-8', errors='ignore')
                else:
                    remote_content = remote_bytes
        except IOError as e:
            print('  ERROR: no pude leer', args.remote_path, '-', e)
            sftp.close(); t.close(); continue

        new_content, changed = replace_block(remote_content, replacement)
        if not changed:
            print('  No se realizó cambio (no se detectó bloque).')
            sftp.close(); t.close(); continue

        timestamp = time.strftime('%Y%m%d%H%M%S')
        backup_remote = args.remote_path + f'.bak.{timestamp}'
        pre_snapshot = args.remote_path + f'.pre_replace_{timestamp}.bak'
        try:
            # move original to backup
            sftp.rename(args.remote_path, backup_remote)
            # write a pre_snapshot copy (for easy inspection)
            with sftp.open(pre_snapshot, 'w') as f:
                f.write(remote_content)
            if args.dry_run:
                sample_name = f'.htaccess.{id_}.new'
                with open(sample_name, 'w', encoding='utf-8') as out:
                    out.write(new_content)
                diff = difflib.unified_diff(
                    remote_content.splitlines(keepends=True),
                    new_content.splitlines(keepends=True),
                    fromfile='orig', tofile='new')
                print('  Dry-run diff (first 200 lines):')
                for i, line in enumerate(diff):
                    if i > 200: break
                    print(line.rstrip('\n'))
                # restore original name from backup so remote not changed
                sftp.rename(backup_remote, args.remote_path)
            else:
                with sftp.open(args.remote_path, 'w') as wf:
                    wf.write(new_content)
                print('  OK: .htaccess reemplazado; backup en', backup_remote)
        except Exception as e:
            print('  ERROR durante backup/escritura:', e)
            try:
                if sftp.stat(backup_remote):
                    try:
                        sftp.rename(backup_remote, args.remote_path)
                        print('  Restaurado desde backup.')
                    except:
                        pass
            except:
                pass
        finally:
            sftp.close(); t.close()

if __name__ == '__main__':
    main()
