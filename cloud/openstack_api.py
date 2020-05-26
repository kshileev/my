class OpenstackClient(object):
    def __repr__(self):
        return f'OS {self.cfg.name}'

    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = self.cfg.logger

    def os_cmds(self, commands):
        import json

        commands = commands if type(commands) is list else [commands]

        cmd = '; echo , ;'.join(commands)
        ans = self.cfg.proxy_server.exe_cmds('source ' + self.cfg.auth.openrc_path + '; ' + cmd)
        try:
            if 'ossqe-helpers' in cmd:
                return json.loads(ans.replace('},\n]', '}]'))
            else:
                return json.loads('[' + ans.strip(',\n') + ']')
        except :
            raise RuntimeError('Something wrong ')

    def analyse_problems(self, obj_l):
        egrep = '"' + '|'.join([o.get('ID') if type(o) is dict else o.os_id for o in obj_l]) + '"'
        self.pod.mgm.exe_cmds(f'. ossqe-helpers ; ossqe_problem {egrep}')

    def final_logs_check(self):
        info = self.status_d.get('info', [])
        if info:
            final_folder = self.collect_info(title='fin')
            diff = final_folder.replace('info_fin', 'info_diff')
            tb = diff.replace('info_diff', 'info_tracebacks')
            self.pod.mgm.exe_cmds([f'diff {info[0]} {final_folder} > {diff}', f'grep Traceback {diff} > {tb}'])
            self.pod.mgm.scp_to_local(remote_paths=[diff, tb])
        return self.pod.check_crash_files()

    def collect_info(self, title):
        title = '_for_' + title + '_of_' + self.pod.mgm.consumer_name
        ans = self.os_cmd(f'. ossqe-helpers;ossqe_collect_logs {title}')
        self.status_d.setdefault('info', [])
        self.status_d['info'].append(ans[0])
        return ans[0]
