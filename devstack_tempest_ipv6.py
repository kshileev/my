#!/usr/bin/env python
# Copyright 2014 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Dane LeBlanc, Cisco Systems, Inc.
#
# Create a DevStack instance and run the Tempest tests listed in
# the file '~/tempest_tests.txt'
#
# Overview:
# (1) Clean up old devstack (unstack)
# (2) Clone devstack if not already present
# (3) Create a localrc file
# (4) Run stack.sh
# (6) Run tempest tests

local_rc_template = '''[[local|localrc]]
MYSQL_PASSWORD=nova
RABBIT_PASSWORD=nova
SERVICE_TOKEN=nova
SERVICE_PASSWORD=nova
ADMIN_PASSWORD=nova
ENABLED_SERVICES=g-api,g-reg,key,n-api,n-crt,n-obj,n-cpu,n-cond,cinder,c-sch,c-api,c-vol,n-sch,n-novnc,n-xvnc,n-cauth,horizon,rabbit
enable_service mysql
disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-l3
enable_service q-dhcp
enable_service q-meta
enable_service q-lbaas
enable_service neutron
enable_service tempest
NOVA_USE_NEUTRON_API=v2
VOLUME_BACKING_FILE_SIZE=2052M
API_RATE_LIMIT=False
VERBOSE=True
DEBUG=True
LOGFILE={0}/stack.sh.log
USE_SCREEN=True
SCREEN_LOGDIR={0}
'''


def print_banner(msg):
    from datetime import datetime

    print '''
    ***************************************
    * {0} *
    ***************************************
    ZULU {1}  UTC {2}'''.format(msg, datetime.now(), datetime.utcnow())


def deploy_devstack(devstack_dir, is_re_clone_devstack, is_v6):
    print_banner('     Deploy DevStack')

    cleanup_previous_devstack(devstack_dir, is_clean_opt=is_re_clone_devstack)
    if is_re_clone_devstack and not os.path.isdir(devstack_dir):
        clone_devstack(devstack_dir)

    create_devstack_config(devstack_dir=devstack_dir, is_reclone=is_re_clone_devstack, is_ipv6=is_v6)

    if is_v6:
        patch_devstack(devstack_dir, '87987')

    run_devstack_dot_stack(devstack_dir)

    # if is_v6:
    #     patch_ipv6_radvd_neutron() #apply 102648
    #     do_restack(devstack_dir)

        # Comment out next 3 lines. Currently no bugs to temporarily patch around.
        #patch_neutron_bugs()
        #restart_neutron_processes()
        #time.sleep(5)


def cleanup_previous_devstack(devstack_dir, is_clean_opt):
    print_banner('Clean up previous DevStack instance')
    if os.path.isdir(devstack_dir):
        os.chdir(devstack_dir)
        run_cmd_line('./unstack.sh', raise_exception_on_error=False)
    for project in ['neutron-', 'nova', 'glance', 'cinder', 'keystone']:
        run_cmd_line('pkill -f %s' % project, raise_exception_on_error=False)
    run_cmd_line('sudo rm /var/lib/dpkg/lock', raise_exception_on_error=False)
    run_cmd_line('sudo rm /var/log/libvirt/libvirtd.log', raise_exception_on_error=False)
    if is_clean_opt:
        remove_subdir('/opt')
        #remove_subdir(devstack_dir)


def do_restack(devstack_dir):
    import time
    import sys

    print_banner('    Re-Stacking (unstack/stack)    ')
    os.chdir(devstack_dir)
    run_cmd_line('./unstack.sh', raise_exception_on_error=False)
    time.sleep(3)
    output, stack_rc = run_cmd_line('./stack.sh', raise_exception_on_error=False)
    if stack_rc:
        print_banner('stack.sh FAILED')
        sys.exit(stack_rc)


def clone_devstack(abs_path_to_clone_to='$HOME/devstack'):
    print_banner('         Cloning DevStack          ')
    run_cmd_line('git clone git://github.com/openstack-dev/devstack.git {0}'.format(abs_path_to_clone_to))


def create_devstack_config(devstack_dir, is_ipv6=True, is_reclone=False):
    print_banner('  Create devstack local.conf  ')

    do_re_clone_flags = '#RECLONE=no\n#OFFLINE=True'
    no_re_clone_flags = 'RECLONE=no\nOFFLINE=True'
    private_ipv6 = 'IP_VERSION=4+6\nIPV6_PRIVATE_RANGE={0}/64\nIPV6_NETWORK_GATEWAY={0}1\nREMOVE_PUBLIC_BRIDGE=False\n'.format('feee:1975::')
    public_ipv6 = 'IPV6_PUBLIC_RANGE={0}/64\nIPV6_PUBLIC_NETWORK_GATEWAY={0}1\n'.format('2005:1975::')

    ipv6 = private_ipv6 + public_ipv6

    body = local_rc_template.format('/opt/stack/logs') + ipv6 if is_ipv6 else '' + do_re_clone_flags if is_reclone else no_re_clone_flags
    with open(devstack_dir + '/local.conf', 'w') as f:
        f.write(body)
    print body


def run_devstack_dot_stack(devstack_dir):
    import sys

    print_banner('Running DevStack ./stack.sh')
    os.chdir(devstack_dir)
    output, stack_rc = run_cmd_line('./stack.sh', raise_exception_on_error=False)
    if stack_rc:
        print_banner('stack.sh FAILED')
        sys.exit(stack_rc)


def remove_subdir(subdir):
    run_cmd_line('sudo rm -rf %s' % subdir, raise_exception_on_error=False)


def patch_devstack(devstack_dir, patch_id):
    print_banner('Applying DevStack Patch: {0}'.format(patch_id))
    os.chdir(devstack_dir)
    output, rc = run_cmd_line('git review -d {0}'.format(patch_id))
    print output


def restart_neutron_processes():
    import re

    print_banner('    Restarting Neutron Processes   ')
    reg_exes = {}
    for proc in ['neutron-server', 'neutron-openvswitch-agent', 'neutron-dhcp-agent', 'neutron-l3-agent', 'neutron-metadata-agent', 'neutron-lbaas-agent']:
        reg_exes[proc] = re.compile(
            "^(?P<uid>\S+)\s+(?P<pid>\d+)\s+(?P<ppid>\d+).*python(?P<cmd>.*%s.*)"
            % proc)
    ps_output, rc = run_cmd_line('ps -ef')
    for line in ps_output.splitlines():
        for proc, reg_ex in reg_exes.items():
            result = reg_ex.search(line)
            if result:
                print 'Found ', proc
                print 'Command line: ', line
                print 'Restarting ', proc
                # Kill the process
                out, rc = run_cmd_line('kill -9 %d' % int(result.group('pid')), raise_exception_on_error=False)
                # Re-run the  process if kill was successful
                if not rc:
                    filename = os.path.join('ipv6-' + proc + '.log')
                    cmd = result.group('cmd') + ' > %s 2>&1 &' % filename
                    print cmd
                    os.system(cmd)
    print 'Neutron processes: '
    ps_output, rc = run_cmd_line('ps -ef')
    for line in ps_output.splitlines():
        for proc, reg_ex in reg_exes.items():
            result = reg_ex.search(line)
            if result:
                print line


def run_cmd_line(cmd_str, std_err=None, shell=False, echo_cmd=True, raise_exception_on_error=True):
    import subprocess
    import sys

    if echo_cmd:
        print cmd_str
    if shell:
        cmd_args = cmd_str
    else:
        cmd_args = cmd_str.split()
    output = None
    return_code = 0
    try:
        output = subprocess.check_output(cmd_args, shell=shell, stderr=std_err)
    except subprocess.CalledProcessError as e:
        if raise_exception_on_error:
            print e
            sys.exit(e.returncode)
        else:
            return_code = e.returncode
    return output, return_code


def run_tempest_tests(test_list_file):
    import os

    print_banner('      Running Tempest Tests       ')
    os.chdir('/opt/stack/tempest/')
    if not os.path.isdir('.testrepository'):
        run_cmd_line('testr init', raise_exception_on_error=False)
    logfile = os.path.join('ipv6_tempest_log.txt')
    print 'Tests to be run:'
    output, rc = run_cmd_line('cat %s' % test_list_file, raise_exception_on_error=False)
    print output
    cmd = 'testr run --load-list=%s > %s' % (test_list_file, logfile)
    print cmd
    result = os.system(cmd)

    print_banner('TEMPEST {0}'.format('PASSED!' if result else 'FAILED'))
    return result == 0


def install_prerequisites():
    out, rc = run_cmd_line('dpkg -l git-review', raise_exception_on_error=False)
    if rc:
        run_cmd_line('sudo apt-get install git-review -y')


def correct_devstack_dir(devstack_dir):
    import os

    abs_dir = os.path.abspath(devstack_dir)
    base_dir = os.path.dirname(abs_dir)
    if os.access(abs_dir, os.W_OK) or os.access(base_dir, os.W_OK):
        return abs_dir
    else:
        raise argparse.ArgumentTypeError('Not possible to clone devstack to {0}'.format(abs_dir))


def correct_tempest_list_file(path):
    import os

    if os.path.isfile(path):
        return os.path.abspath(path)
    else:
        raise argparse.ArgumentTypeError('Could not read file {0}'.format(path))


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Install devstack and run tempests if provided by user')
    parser.add_argument('--devstack-dir', default=os.path.expanduser('~/devstack'), type=correct_devstack_dir, help='folder where to clone devstack')
    parser.add_argument('--is-re-clone', default=True, type=bool, help='do we need to re-clone devstack')
    parser.add_argument('--is-v6', default=True, type=bool, help='do we need apply to configure in ipv6')
    parser.add_argument('tempest_list_file', default=None, nargs='?', type=correct_tempest_list_file, help='file which lists tempests to execute')
    args = parser.parse_args()

    install_prerequisites()
    deploy_devstack(devstack_dir=args.devstack_dir, is_re_clone_devstack=args.is_re_clone, is_v6=args.is_v6)
    if args.tempest_list_file:
        run_tempest_tests(args.tempest_list_file)