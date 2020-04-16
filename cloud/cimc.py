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


class CimcChassis:
    def __init__(self, full_body):
        self.body = full_body

    def __repr__(self):
        return f'change me'


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


class CimcCtl:
    def __init__(self, full_body):
        self.body = full_body

        d = {y[0]: y[1] for y in [x.strip().split(': ') for x in self.body.split('\r\n') if ':' in x] if len(y) == 2}
        self.ip4 = d['IPv4 Address']
        self.ip6 = d['IPv6 SLAAC Address']
        self.mac = d['MAC Address']
        self.hostname = d['Hostname']
        self.serial = d['Serial Number']
        self.power = d['Power']

    def __repr__(self):
        return f'change me'


class CimcInfo:
    def __init__(self, body):
        self.body = body
        self._ctl = None
        self._physical = None
        self._virtual = None


    @property
    def ctl(self):
        if not self._ctl:
            self._ctl = CimcCtl(full_body=self.body)
        return self._ctl

    def __repr__(self):
        return f'CimcInfo {self.ctl.ip4}'

    @property
    def physical(self):
        if not self._physical:
            cards = [x for x in self.body.split('Supported')[1].split('\r\n') if x[0] in ['0', '1', 'e', 't', 's', 'p', 'm']]
            self._physical = [CimcNicPhysical(x.split()) for x in cards if x[0] in ['0', '1']]
        return self._physical

    @property
    def virtual(self):
        if not self._virtual:
            cards = [x for x in self.body.split('Supported')[1].split('\r\n') if x[0] in ['0', '1', 'e', 't', 's', 'p', 'm']]
            self._virtual = [CimcNicVirtual(x.split()) for x in cards if x[0] not in ['0', '1']]
        return self._virtual

    @property
    def macs(self):
        return [x.mac for x in self.physical + self.virtual] + [self.ctl.mac]


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
        return CimcInfo(body=rf_cimc_info + rf_cards_info)

    def get_info(self):
        a = self.exe_cmds(['scope cimc/network', 'show detail', 'top', 'scope chassis', 'show detail', 'show network-adapter', 'show adapter',
                           'scope adapter MLOM', 'show ext-eth-if', 'show host-eth-if',
                           'scope adapter 1', 'show ext-eth-if', 'show host-eth-if',
                           'scope adapter 2', 'show ext-eth-if', 'show host-eth-if'])
        return CimcInfo(body=a)


class Cimcs:
    def __init__(self, cimcs):
        self.cimcs = cimcs

    def __repr__(self):
        return f'n={len(self.cimcs)}'

    def verify_all_parameters(self):
        import multiprocessing

        pool = multiprocessing.Pool(processes=10)
        infos = pool.map(pull_get_cimc_info, self.cimcs)
        for cimc, info in zip(self.cimcs, infos):
            cimc.info = info

        new_cfg_d = [{'ip4': x.info.ip4, 'ip6': x.info.slaac, 'name': x.info.hostname, 'uname': x.cfg.uname, 'passwd': x.cfg.passwd, 'serial': x.info.serial} for x in self.cimcs]
        print('cimc:')
        [print(f'- {x}') for x in new_cfg_d]


def pull_get_cimc_info(cimc):
    return cimc.get_info()
