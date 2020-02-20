def execute(ip, uname, passwd, commands, proxy_ip):
    import paramiko
    import time

    if proxy_ip:
        proxy = paramiko.SSHClient()
        proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        proxy.connect(hostname=f'{proxy_ip}', username='root', password=passwd, timeout=15)
    else:
        proxy = None

    remote = paramiko.SSHClient()
    remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if proxy:
        proxy_sock = proxy.get_transport().open_channel('direct-tcpip', (ip, 22), ('127.0.0.1', 10022))
        remote.connect(hostname=f'{ip}', username=uname, password=passwd, sock=proxy_sock, timeout=15)
    else:
        remote.connect(hostname=f'{ip}', username=uname, password=passwd, timeout=15)
    shell = remote.invoke_shell(width=1024, height=600)
    shell.sendall(commands + '\n')

    a = b''
    while True:  # first wait for mgm root prompt
        if shell.recv_ready():
            a += shell.recv(1024)
        if a.endswith(b' # '):
            break
        time.sleep(1)
    remote.close()
    if proxy:
        proxy.close()
    return a.decode('utf-8')

def main():
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True)
    parser.add_argument('--proxy_ip', type=str)
    parser.add_argument('--uname', type=str, default='admin')
    parser.add_argument('--passwd', type=str, required=True)
    parser.add_argument('commands', nargs='+', help='list of separated commands to execute, separators: ; +')

    args = parser.parse_args()

    cmd = ' '.join(args.commands).replace(';', '\n').replace('+', '\n')
    ans = execute(ip=args.ip, uname=args.uname, passwd=args.passwd, commands=cmd, proxy_ip=args.proxy_ip)
    d = {y[0]: y[1] for y in [x.strip().split(': ') for x in ans.split('\r\n') if ':' in x] if len(y) == 2}
    print(json.dumps(d))


if __name__ == '__main__':
    main()
