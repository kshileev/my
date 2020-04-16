class PodCfg:
    def __init__(self, name, cfg_d):
        from cloud.root_logger import create_base_logger
        from cloud.tor_cfg import TorsCfg
        from cloud.cimc_cfg import CimcsCfg
        from cloud.server import ServerCfg

        self.name = name
        self.cfg_d = cfg_d
        self.logger = create_base_logger(name=self.name)
        self.tors = TorsCfg(pod_cfg=self)
        self.cimcs = CimcsCfg(pod_cfg=self)
        self.mgm = ServerCfg(name=f'{self.name}.mgm', ip=self.cfg_d['mgm']['ip4'], uname=self.cfg_d['mgm']['uname'], passwd=self.cfg_d['mgm']['passwd'])

    def __repr__(self):
        return f'{self.name} CFG'

    def os(self):
        from cloud.os_cfg import OsCfg

        return OsCfg(pod_cfg=self)

    @classmethod
    def from_cfg_file(cls, stream):
        import yaml
        import os

        cfg_d = yaml.safe_load(stream)
        pod_name = os.path.basename(stream.name).replace('.spec', '').replace('.yaml', '').replace('CFG.', '')
        return cls(name=pod_name, cfg_d=cfg_d)

    def print(self):
        [x.print(pod_cfg=self) for x in self.tors if x.role in ['a', 'b']]

    def create_pod(self):
        return Pod(cfg=self)


class Pod:
    def __init__(self, cfg):
        self.cfg = cfg
        self._mgm = None
        self._cimcs = None
        self._os = None

    def __repr__(self):
        return self.cfg.name

    def mgm(self):
        if not self._mgm:
            self._mgm = self.cfg.mgm().create_server()
        return self._mgm

    def cimcs(self):
        if not self._cimcs:
            self._cimcs = self.cfg.cimcs().create_them(proxy=self.mgm())
        return self._cimcs

    def os(self):
        if not self._os:
            self._os = self.cfg.os().create_os_client(proxy=self.mgm())
        return self._os
