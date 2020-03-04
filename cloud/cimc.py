from cloud import server


class CimcNicPhysical:
    def __init__(self, lst):
        self.id = f'MLOM{lst[0]}'
        self.mac = lst[1]
        self.status = lst[2]
        self.admin_speed = lst[4]
        self.real_speed = lst[5]

    def __repr__(self):
        return f'{self.id} {self.status}'


class CimcNicVirtual:
    def __init__(self, lst):
        self.id = lst[0]
        self.mtu = lst[1]
        self.mlom_id = f'MLOM{lst[2]}'
        self.mac = lst[3]
        self.cos = lst[4]
        self.vlan = lst[5]
        self.pxe_boot = lst[6]

    def __repr__(self):
        return f'{self.id}@{self.mlom_id}'


class CimcInfo:
    def __init__(self, d):
        self.d = d

    def __repr__(self):
        return f'CimcInfo {self.ip4}'

    @property
    def ip4(self):
        return self.d['cimc']['IPv4 Address']

    @property
    def slaac(self):
        return self.d['cimc']['IPv6 SLAAC Address']

    @property
    def mac(self):
        return self.d['cimc']['MAC Address']

    @property
    def hostname(self):
        return self.d['cimc']['Hostname']

    @property
    def serial(self):
        return self.d['cimc']['Serial Number']

    @property
    def power(self):
        return self.d['cimc']['Power']

    @property
    def physical(self):
        return self.d['nics'][:2]

    @property
    def virtual(self):
        return self.d['nics'][3]


class CimcCfg(server.ServerCfg):
    @classmethod
    def from_cfg_d(cls, pod_cfg, cfg_d):

        ip = cfg_d.get('ip6') or cfg_d.get('ip4')
        name = f'{cfg_d["name"]}.cimc'
        if pod_cfg.name not in name:
            name = f'{pod_cfg.name}.{name}'
        cimc_cfg =cls(name=name, ip=ip, uname=cfg_d['uname'], passwd=cfg_d['passwd'])
        cimc_cfg.serial = cfg_d.get('serial')
        return cimc_cfg

    def create_server(self, proxy=None):
        return Cimc(cfg=self, proxy=proxy)


class Cimc(server.Server):
    is_via_shell = True

    def get_redfish(self):
        from cloud.curl import Curl

        curl = Curl(logger=self.cfg.logger)
        if not self.cfg.serial:
            rf_base = curl.curl_get(url=f'https://[{self.cfg.ip}]/redfish/v1/Systems', uname=self.cfg.uname, passwd=self.cfg.passwd)
            system_url = rf_base.json()['Members'][0]['@odata.id']
        else:
            system_url = f'/redfish/v1/Systems/{self.cfg.system}'

        rf_cimc_info = curl.curl_get(url=f'https://[{self.cfg.ip}]/redfish/v1/Managers/CIMC/EthernetInterfaces/NICs', uname=self.cfg.uname, passwd=self.cfg.passwd)
        rf_cards_info = [curl.curl_get(url=f'https://[{self.cfg.ip}]{system_url}/EthernetInterfaces/{card}', uname=self.cfg.uname, passwd=self.cfg.passwd) for card in ['MLOM.0', 'MLOM.1']]
        return CimcInfo(d={'cimc': rf_cimc_info.json(), 'mlom': [x.json() for x in rf_cards_info]})

    def get_info(self):
        a = self.exe_cmds(['scope cimc/network', 'show detail', 'top', 'scope chassis', 'show detail', 'scope adapter MLOM', 'show ext-eth-if', 'show host-eth-if'])
        cimc = {y[0]: y[1] for y in [x.strip().split(': ') for x in a.split('\r\n') if ':' in x] if len(y) == 2}
        cards = [x for x in a.split('Supported')[1].split('\r\n') if x[0] in ['0', '1', 'e', 't', 's', 'p', 'm']]
        physical = [CimcNicPhysical(x.split()) for x in cards if x[0] in ['0', '1']]
        virtual = [CimcNicVirtual(x.split()) for x in cards if x[0] not in ['0', '1']]
        return CimcInfo(d={'cimc': cimc, 'nics': physical + virtual})


class CimcsCfg:
    def __init__(self, pod_cfg):
        self.cfg_d = pod_cfg.cfg_d['cimc']
        self.cfgs = [CimcCfg.from_cfg_d(pod_cfg=pod_cfg, cfg_d=x) for x in self.cfg_d]

    def __repr__(self):
        return f'n={len(self.cfg_d)}'

    def create_them(self, proxy=None):
        return Cimcs([x.create_server(proxy=proxy) for x in self.cfgs])


class Cimcs:
    def __init__(self, cimcs):
        self.cimcs = cimcs

    def __repr__(self):
        return f'n={len(self.cimcs)}'

    def verify_all_parameters(self):
        import multiprocessing

        pool = multiprocessing.Pool(processes=10)
        a = pool.map(pull_get_cimc_info, self.cimcs)
        for cimc, info in zip(self.cimcs, a):
            cimc.info = info

        new_cfg_d = [{'ip4': x.info.ip4, 'ip6': x.info.slaac, 'name': x.info.hostname, 'uname': x.cfg.uname, 'passwd': x.cfg.passwd, 'serial': x.info.serial} for x in self.cimcs]
        print('cimc:')
        [print(f'- {x}') for x in new_cfg_d]


def pull_get_cimc_info(cimc):
    return cimc.get_info()
