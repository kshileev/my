from cloud import server


class TorCfg(server.ServerCfg):  # config of a single TOR
    def __init__(self, cfg_d):
        self.cfg_d = cfg_d
        super(TorCfg, self).__init__(name=cfg_d['role'], ip=cfg_d['ip4'], uname=cfg_d['uname'], passwd=cfg_d['passwd'])

    @property
    def role(self):
        return self.cfg_d['role']

    def print(self, pod_cfg):
        print('start config for', self.name, self.ip, ':\n')
        print(f'sh int st | i {pod_cfg.name[:3]}')
        for cimc_cfg in pod_cfg.cimcs:
            print('int', cimc_cfg.links[self.role])
            print('description', pod_cfg.name[:3], cimc_cfg.ip)
            if cimc_cfg.role != 'iron':
                po_id = cimc_cfg.links[self.role].split('/')[-1]
                print('int po', po_id)
                print('description', pod_cfg.name[:3], cimc_cfg.ip)
                print('switchport mode trunk')
                print('switchport trunk allowed vlan')
                print('spanning-tree port type edge trunk')
                print('mtu 9216')
                print('no lacp suspend-individual')
                print('vpc', po_id)
                print()
            else:
                print('heh hey')

            print()
        print(f'sh int st | i {pod_cfg.name[:3]}')
        print('\nend config for', self.name, self.ip, '\n')


class TorsCfg:
    def __init__(self, pod_cfg):
        self.cfg_l = pod_cfg.cfg_d.get('tors', {})
        self.cfgs = []
        for tor_d in self.cfg_l:
            self.cfgs.append(TorCfg(cfg_d=tor_d))

    def __iter__(self):
        return iter(self.cfgs)

    def __repr__(self):
        return f'{len(self.cfgs)} TORs'
