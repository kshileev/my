class ServerCfg(object):
    def __init__(self, name, ip, uname, passwd):
        from cloud.root_logger import create_component_logger

        self.name, self.ip, self.uname, self.passwd = name, ip, uname, passwd
        self.logger = create_component_logger(name=self.name)

    def create_server(self, proxy=None):
        return Server(cfg=self, proxy=proxy)

    def __repr__(self):
        return self.name


class Server(object):
    def __init__(self, cfg, proxy=None):
        self.cfg, self.proxy = cfg, proxy

        self._ssh_client = None

    def __repr__(self):
        add = f' -J {self.proxy.cfg.uname}@{self.proxy.cfg.name} '.replace('.', '.ssh.') if self.proxy else ' '
        return f'{self.cfg.name}: ( sshpass -p {self.cfg.passwd} ssh{add}{self.cfg.uname}@{self.cfg.ip} )'

    def ssh_client(self):
        import paramiko

        if self._ssh_client is None:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                if self.proxy:
                    proxy_sock = self.proxy.ssh_client().get_transport().open_channel('direct-tcpip', (self.cfg.ip, 22), ('127.0.0.1', 10022))
                    self._ssh_client.connect(hostname=str(self.cfg.ip), username=self.cfg.uname, password=self.cfg.passwd, timeout=15, sock=proxy_sock)
                    self.cfg.logger.debug(f'connected via {self.proxy.cfg.name}')
                else:
                    self._ssh_client.connect(hostname=str(self.cfg.ip), username=self.cfg.uname, password=self.cfg.passwd, timeout=15)
                    self.cfg.logger.debug('connected')
            except Exception as ex:
                self.cfg.logger.error(f'{self}: fail to connect, in paramiko: {type(ex)} {ex}')
                raise RuntimeError(f'failed to connect to {self}, paramiko error: {ex}')
        return self._ssh_client

    def exe_cmds(self, cmds, is_with_tty=False, is_in_background=False):
        import time

        if type(cmds) is not list:
            cmds = [cmds]
        sep = ' ; echo ++ ; '
        if is_in_background:
            paths = [x.replace('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null', '').replace(' ', '_').replace('-', '_').replace("'", '').replace('/', '_') + '.log' for x in cmds]
            cmds = [f'nohup {x[0]} > {x[1]} 2>&1 &' for x in zip(cmds, paths)]
        else:
            paths = []
        cmd = sep.join(cmds)
        ssh = self.ssh_client()

        try:
            self.cfg.logger.debug(f'{cmd} .......')
            if hasattr(self, 'is_via_shell'):
                shell = ssh.invoke_shell(width=1024, height=600)
                shell.sendall('\n'.join(cmds) + '\n')

                a = b''
                n_waits_for_finish = 0
                while True:
                    if shell.recv_ready():
                        a += shell.recv(1024)
                        n_waits_for_finish = 0
                    if n_waits_for_finish == 5:  # consider command finished after 5 times with no bytes received
                        break
                    time.sleep(1)
                    n_waits_for_finish += 1
                out = a.decode('utf-8')
                self.cfg.logger.debug(f'{cmd} >>>>>>>\n\n\n{out or "no output"}\n\n\n++++++++++++ end of output +++++++++++++++++')
                return out
            else:
                stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=is_with_tty)
                err = stderr.read().decode('utf-8')
                err = err.split('Warning: Permanently added')[0]  # suppress Warning
                err = err.split('/etc/profile.d/autologout.sh: line 1: TMOUT: readonly variable\n')[-1]  # suppress
                out = stdout.read().decode('utf-8')
                outputs = []
                for c, o in zip(cmds, (out + err).split('++')):
                    o = o.strip('\n')
                    self.cfg.logger.debug(f'{c} >>>>>>>\n\n\n{o or "no output"}\n\n\n++++++++++++ end of output +++++++++++++++++')
                    outputs.append(o)
                if is_in_background:
                    outputs = [x[0] if x[0] else x[1] for x in zip(outputs, paths)]

                if is_in_background:
                    return paths[0] if len(paths) == 1 else paths
                else:
                    return outputs[0] if len(outputs) == 1 else outputs
        except Exception as ex:
            self.cfg.logger.error(f'in Server.exe_cmds {cmd} except: {ex}')
            raise RuntimeError(str(ex))


class ServerNic(object):
    def __init__(self, server, nic_id, mac):
        self.mac = mac
        self.server = server
        self.nic_id = nic_id

    def __repr__(self):
        return f'{self.server.name}.{self.nic_id}: {self.mac_cisco_style}'

    @property
    def mac_cisco_style(self):
        return f'{self.mac[0:2]}{self.mac[3:5]}.{self.mac[6:8]}{self.mac[9:11]}.{self.mac[12:14]}{self.mac[15:17]}'.lower()
