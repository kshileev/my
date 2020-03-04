class PodCfg:
    def __init__(self, name, cfg_d):
        from cloud.root_logger import create_base_logger

        self.name = name
        self.cfg_d = cfg_d
        self.logger = create_base_logger(name=self.name)

    def __repr__(self):
        return f'{self.name} CFG'

    def mgm(self):
        from cloud.server import ServerCfg

        return ServerCfg(name=f'{self.name}.mgm', ip=self.cfg_d['mgm']['ip6'], uname=self.cfg_d['mgm']['uname'], passwd=self.cfg_d['mgm']['passwd'])

    def cimcs(self):
        from cloud.cimc import CimcsCfg

        return CimcsCfg(pod_cfg=self)

    def os(self):
        from cloud.os_cfg import OsCfg

        return OsCfg(pod_cfg=self)

    @classmethod
    def from_yaml_file(cls, stream):
        import yaml
        import os

        cfg_d = yaml.safe_load(stream)
        pod_name = os.path.basename(stream.name).replace('.spec', '').replace('.yaml', '').replace('CFG.', '')
        return cls(name=pod_name, cfg_d=cfg_d)

    def create_pod(self):
        return Pod(cfg=self)


class Pod:
    def __init__(self, cfg):
        self.cfg = cfg
        self.mgm = self.cfg.mgm().create_server()
        self.cimcs = self.cfg.cimcs().create_them() if 'cimcs' in self.cfg.cfg_d else None
        self.os = self.cfg.os().create_os_client(proxy=self.mgm)
