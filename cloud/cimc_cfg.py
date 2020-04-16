from cloud import server


class CimcCfg(server.ServerCfg):  # config of a single CIMC micro-server
    def __init__(self, cfg_d):
        self.cfg_d = cfg_d
        super(CimcCfg, self).__init__(name=cfg_d['role'] + cfg_d['ip4'], ip=cfg_d['ip4'], uname=cfg_d['uname'], passwd=cfg_d['passwd'])

    @property
    def model(self):
        return self.cfg_d.get('model')

    @property
    def role(self):
        return self.cfg_d.get('role')

    @property
    def links(self):
        return self.cfg_d.get('links')


class CimcsCfg:
    def __init__(self, pod_cfg):
        self.cfg_d = pod_cfg.cfg_d.get('cimc')
        self.cfgs = []
        for cimc_d in self.cfg_d:
            self.cfgs.append(CimcCfg(cfg_d=cimc_d))

    def __repr__(self):
        return f'{len(self.cfgs)} CIMCs'

    def __iter__(self):
        return iter(self.cfgs)
