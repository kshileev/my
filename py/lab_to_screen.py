def main():
    """Creates a number of config files for GNU screen utility"""
    from netaddr import IPNetwork
    import yaml
    import os

    def form_window_line():
        first_part = 'screen -t {name} {number} '.format(name=role+str(i), number=screen_num)
        cmd_part = 'ssh {username}@{ip}'.format(username=username, ip=ip)
        return first_part + cmd_part

    script_dir = os.getcwd()
    sqe_repo_dir = None
    for di in [os.path.expanduser('~/os/sqe'), os.path.join(script_dir, '../openstack-sqe')]:
        if os.path.isdir(di):
            sqe_repo_dir = os.path.normpath(di)
            break

    with open(os.path.normpath(os.path.join(script_dir, 'screenrc'))) as f:
        screen_tmpl_body = f.read()

    for lab in ['g8', 'g10']:
        additional_windows = []
        screen_num = 2
        with open(os.path.normpath(os.path.join(sqe_repo_dir, 'lab/configs/labs/{0}.yaml'.format(lab)))) as f:
            lab_cfg = yaml.load(f)

            ip = lab_cfg['ucsm']['host']
            username = lab_cfg['ucsm']['username']
            role = 'ucsm'
            i = ''
            additional_windows.append(form_window_line())
            screen_num += 1

            ip = lab_cfg['n9k']['host']
            username = lab_cfg['n9k']['username']
            role = 'n9k'
            i = 1
            additional_windows.append(form_window_line())
            screen_num += 1

            user_net = IPNetwork(lab_cfg['nets']['user']['cidr'])
            for role, val in lab_cfg['nodes'].iteritems():
                username = 'root' if 'director' in role else 'heat-admin'
                for i, server_id in enumerate(val['server-id']):
                    ip = user_net[val['ip-shift'][i]]
                    additional_windows.append(form_window_line())
                    screen_num += 1
        with open(os.path.expanduser('~/{0}.screen'.format(lab)), 'w') as f:
            f.write(screen_tmpl_body.replace('# here goes additional config', '\n'.join(additional_windows)))


if __name__ == '__main__':
    main()
