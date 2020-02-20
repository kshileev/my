from cloud.server import Server


class Cimc(Server):
    def __init__(self, ip, uname, passwd):
        self.ip, self.uname, self.passwd = ip, uname, passwd
        if ':' in self.ip:
            self.ip = '[' + self.ip + ']'


class Cimcs:
    def __init__(self, cimcs, proxy_srv):
        self.cimcs = cimcs
        self.proxy_srv = proxy_srv

    def __repr__(self):
        return f'{len(self.cimcs)} CIMC servers'

    def learn_nics_in_redfish(self):
        import multiprocessing
        from cloud.server import ServerNic

        pool = multiprocessing.Pool(processes=10)
        hosts = [(h.os_id, f'curl -k -u {h.uname}:{h.passwd} https://{h.ip}') for h in self.cimcs]
        if hosts:
            redfish_info = pool.map(redfish_curl, hosts)
            for single in redfish_info:
                host_name = single[0]
                host = pod.hosts_d[host_name]
                host.nics = [ServerNic(server=host, nic_id=x['Id'], mac=x['PermanentMACAddress']) for x in single[1]]
    @classmethod
    def from_spec_d(cls, cimc_spec, proxy_srv):
        cimcs = [Cimc(ip=x.get('ip4'), uname=x.get('uname'), passwd = x.get('passwd')) for x in cimc_spec]

        return cls(cimcs=cimcs, proxy_srv=proxy_srv)

    def verify_all_parameters(self):
        a = self.proxy_srv.exe_cmds(f'sshpass -p {self.cimcs[0].passwd} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {self.cimcs[0].uname}@{self.cimcs[0].ip} scope cimc/network')
        pass


def redfish_curl(host_name_curl_cmd):
    import subprocess
    import json

    host_name, curl_cmd = host_name_curl_cmd
    systems_url = curl_cmd + '/redfish/v1/Systems'
    systems_text = subprocess.check_output(systems_url.split())
    try:
        systems = json.loads(systems_text)
        system_uuid = systems['Members'][0]['@odata.id'].split('/')[-1]
    except json.decoder.JSONDecodeError as ex:
        raise RuntimeError(f'{host_name}:{systems_url} json decode failed: {systems_text}')
    except KeyError:
        raise RuntimeError(f'{host_name}:{systems_url} has no Members: {systems_text}')
    ifaces = json.loads(subprocess.check_output((curl_cmd + f'/redfish/v1/Systems/{system_uuid}/EthernetInterfaces').split()))

    return host_name, [json.loads(subprocess.check_output((curl_cmd + f'{x["@odata.id"]}').split())) for x in ifaces['Members']]
