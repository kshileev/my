class OsCfg:
    def __init__(self, pod_cfg):
        if 'openrc' in pod_cfg.cfg_d:
            openrc_d = pod_cfg.cfg_d['openrc']
            self.OS_CACERT = openrc_d['OS_CACERT']
            self.OS_AUTH_URL = openrc_d['OS_AUTH_URL']
            self.OS_USERNAME = openrc_d['OS_USERNAME']
            self.OS_PASSWORD = openrc_d['OS_PASSWORD']
            self.OS_REGION_NAME = openrc_d['OS_REGION_NAME']
            self.OS_PROJECT_NAME = openrc_d['OS_PROJECT_NAME']
            self.OS_PROJECT_DOMAIN_NAME = openrc_d['OS_PROJECT_DOMAIN_NAME']
            self.OS_USER_DOMAIN_NAME = openrc_d['OS_USER_DOMAIN_NAME']
            self.OS_IDENTITY_API_VERSION = openrc_d['OS_IDENTITY_API_VERSION']
        else:
            self.OS_CACERT = None
            self.OS_AUTH_URL = None
            self.OS_USERNAME = None
            self.OS_PASSWORD = None
            self.OS_REGION_NAME = None
            self.OS_PROJECT_NAME = None
            self.OS_PROJECT_DOMAIN_NAME = None
            self.OS_USER_DOMAIN_NAME = None
            self.OS_IDENTITY_API_VERSION = None
        self.private_key = None

    def modify_from_openrc_body(self, body):
        for attr_value in [x.split()[1] for x in body.split('\n') if 'export' in x]:
            attr, value = attr_value.split('=')
            setattr(self, attr, value)

    def get_private_key(self, srv):
        if self.private_key is None:
            self.private_key = srv.exe_cmds(cmds=f'cat {self.OS_CACERT}')
        return self.private_key

    def create_os_client(self, proxy):
        from cloud.openstack_client import OpenstackClient

        if self.OS_AUTH_URL is None:
            ans = proxy.exe_cmds(cmds='find . -name openrc -exec grep export {} +')
            self.modify_from_openrc_body(body=ans)
            self.get_private_key(srv=proxy)
            self.get_private_key(srv=proxy)
        return OpenstackClient(cfg=self)
