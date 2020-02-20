class ServerCfg(object):
    def __init__(self, name, ip, uname, passwd, proxy=None):
        self.name = name
        self.ip = ip
        self.uname = uname
        self.passwd = passwd
        self.proxy = proxy

    def create_server(self):
        return Server(cfg=self)


class Server(object):
    def __init__(self, cfg):
        from cloud.root_logger import create_node_logger
        self.cfg = cfg

        self._sshcon = None
        self.logger = create_node_logger(name=self.cfg.name)

    def __repr__(self):
        return f'{self.cfg.name}: (sshpass -p {self.cfg.passwd} ssh {self.cfg.uname}@{self.cfg.ip}'

    @property
    def pkey(self):
        import os
        import paramiko

        if self._pkey is None:
            repo_dir = os.path.dirname(os.path.dirname(__file__))
            key_path = os.path.join(repo_dir, 'etc', 'keys', 'kir_no_secret')
            self._pkey = paramiko.RSAKey.from_private_key_file(key_path)
        return self._pkey

    @property
    def sshcon(self):
        import paramiko

        if self._sshcon is None:
            self._sshcon = paramiko.SSHClient()
            self._sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self._sshcon.get_transport() is None or not self._sshcon.get_transport().is_active():
            try:
                if self.cfg.passwd:
                    self._sshcon.connect(hostname=str(self.cfg.ip), username=self.cfg.uname, password=self.cfg.passwd, timeout=5, look_for_keys=False)
                else:
                    self._sshcon.connect(hostname=str(self.cfg.ip), username=self.cfg.uname, pkey=self.pkey, timeout=5, look_for_keys=False)
                self.logger.debug('connected')
            except Exception as ex:
                self.logger.error('{}: fail to connect {}'.format(self, ex))
                raise RuntimeError(ex)
        return self._sshcon

    def exe_cmds(self, cmds, is_with_tty=False, is_in_background=False):
        if type(cmds) is not list:
            cmds = [cmds]
        sep = ' ; echo ++ ; '
        if is_in_background:
            paths = [x.replace('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null', '').replace(' ', '_').replace('-', '_').replace("'", '').replace('/', '_') + '.log' for x in cmds]
            cmds = [f'nohup {x[0]} > {x[1]} 2>&1 &' for x in zip(cmds, paths)]
        else:
            paths = []
        cmd = sep.join(cmds)
        if hasattr(self, 'via_host'):
            sshcon = self.via_host.sshcon
            cmd = f'ssh -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {self.os_id} ' + cmd
        else:
            sshcon = self.sshcon

        try:
            self.logger.debug(f'{cmd} .......')
            stdin, stdout, stderr = sshcon.exec_command(cmd, get_pty=is_with_tty)
            err = stderr.read().decode('utf-8')
            err = err.split('Warning: Permanently added')[0]  # suppress Warning
            err = err.split('/etc/profile.d/autologout.sh: line 1: TMOUT: readonly variable\n')[-1]  # suppress
            out = stdout.read().decode('utf-8')
            outputs = []
            for c, o in zip(cmds, (out + err).split('++')):
                o = o.strip('\n')
                self.logger.debug(f'{c} >>>>>>>\n\n\n{o or "no output"}\n\n\n++++++++++++ end of output +++++++++++++++++')
                outputs.append(o)
            if is_in_background:
                outputs = [x[0] if x[0] else x[1] for x in zip(outputs, paths)]

            if is_in_background:
                return paths[0] if len(paths) == 1 else paths
            else:
                return outputs[0] if len(outputs) == 1 else outputs
        except Exception as ex:
            self.logger.error(f'in Server.exe_cmds {cmd} except: {ex}')
            raise RuntimeError(str(ex))

    def close(self):
        self.sshcon.close()

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
