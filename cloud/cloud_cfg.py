class OpenstackAuth:
    def __init__(self, body):
        self.OS_CACERT, self.OS_AUTH_URL, self.OS_USERNAME, self.OS_PASSWORD, self.OS_REGION_NAME, \
        self.OS_PROJECT_NAME, self.OS_PROJECT_DOMAIN_NAME, self.OS_USER_DOMAIN_NAME, self.OS_IDENTITY_API_VERSION = None, None, None, None, None, None, None, None, None
        for attr_value in [x.split()[1] for x in body.split('\n') if 'export' in x]:
            attr, value = attr_value.split('=')
            setattr(self, attr, value)
        self.openrc_path = body.split(':')[0]


class CloudCfg(object):
    def __init__(self, name, proxy_server):
        self.cloud_name = name
        self.logger = self.create_logger()
        self.proxy_server = proxy_server
        self.logger.info('constructing...')
        self.auth = None

    @classmethod
    def from_etc_cfg_yaml(cls, file_name):
        import os
        import yaml
        from cloud import ETC_DIR
        from cloud.server import ServerCfg

        long_name = file_name if file_name.startswith('CFG.') else 'CFG.' + file_name
        long_name = long_name if long_name.endswith('.yaml') else long_name + '.yaml'

        with open(os.path.join(ETC_DIR, long_name)) as f:
            cfg_d = yaml.safe_load(f)
        cloud_name = cfg_d['pod']['name']
        entry = ServerCfg(name=cloud_name + '.main',
                          ip=cfg_d['pod']['entry']['ip'],
                          uname=cfg_d['pod']['entry']['uname'],
                          passwd=cfg_d['pod']['entry'].get('passwd'),
                          ).create_server()
        return cls(name=cloud_name, proxy_server=entry)

    def create_cloud_client(self):
        from cloud.openstack_client import OpenstackClient

        ans = self.proxy_server.exe_cmds(cmds='find . -name openrc -exec grep export {} +')
        self.auth = OpenstackAuth(body=ans)
        return OpenstackClient(cfg=self)

    def create_logger(self):
        import logging
        import os
    
        logger = logging.getLogger(self.cloud_name)
        logger.setLevel(logging.DEBUG)
        stream_handler_candidates = [x for x in logger.handlers if type(x) == logging.StreamHandler]
        file_handler_candidates = [x for x in logger.handlers if type(x) == logging.FileHandler]
        formatter = logging.Formatter(fmt='{name}: {message}', style='{')
        if len(stream_handler_candidates) == 0:
            st_hdl = logging.StreamHandler()
            st_hdl.setLevel(logging.DEBUG)
            st_hdl.setFormatter(fmt=formatter)
            logger.addHandler(st_hdl)
        if len(file_handler_candidates) == 0:
            os.system('mkdir -p artifacts')
            file_hdl = (logging.FileHandler(filename=os.path.join('artifacts', self.cloud_name + '_debug.log'), mode='w'))
            file_hdl.setLevel(logging.DEBUG)
            file_hdl.setFormatter(fmt=formatter)
            logger.addHandler(file_hdl)
        return logger
