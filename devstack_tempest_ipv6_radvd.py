# Copyright 2014 Cisco Systems, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
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
# the 'tempest_list-file'
#
# Overview:
# (1) Clean up old devstack (unstack)
# (2) Clone devstack if not already present
# (3) Create a localrc file
# (4) Run stack.sh
# (6) Run tempest tests

import os
import re
import subprocess
import sys
import time


test_list_file = '/home/leblancd/ipv6_tempest/tempest_tests.txt'
log_prefix = 'ipv6'
log_path = '/opt/stack/logs'
devstack_repo = 'git://github.com/openstack-dev/devstack.git'
cleanup_kill_projects = ['neutron-', 'nova', 'glance',
                         'cinder', 'keystone']
neutron_restart_procs = [
    'neutron-server', 'neutron-openvswitch-agent',
    'neutron-dhcp-agent', 'neutron-l3-agent',
    'neutron-metadata-agent', 'neutron-lbaas-agent']
openstack_dir = '/opt/stack/'
neutron_dir = openstack_dir + 'neutron/'
tempest_dir = openstack_dir + 'tempest/'
cleanup_libvirt_log = '/var/log/libvirt/libvirtd.log'
cleanup_dpkg_lock = '/var/lib/dpkg/lock'
neutron_log_file = 'ipv6-neutron-server.log'

banner_fmt = '''
    ***************************************
    * %s *
    ***************************************'''

do_reclone = False

localrc_tempest = '''
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
LOGFILE=%s/stack.sh.log
USE_SCREEN=True
SCREEN_LOGDIR=%s
IP_VERSION=4+6
IPV6_PRIVATE_RANGE=2001:420:2c50:200b::/64
IPV6_NETWORK_GATEWAY=2001:420:2c50:200b::1
REMOVE_PUBLIC_BRIDGE=False
'''

do_reclone_flags = '''
#RECLONE=no
#OFFLINE=True
'''

no_reclone_flags = '''
RECLONE=no
OFFLINE=True
'''


def print_date():
    output, rc = run_cmd_line('date --utc', echo_cmd=False, check_result=False)
    print output

def print_banner(msg):
    print banner_fmt % msg
    print_date()

def run_devstack_and_tempest():
    print_banner('     Run DevStack and Tempest      ')

    devstack_dir = os.path.expanduser('~/devstack')
    localrc_path = os.path.expanduser('~/devstack/localrc')

    cleanup_previous_devstack(devstack_dir)
    if do_reclone and not os.path.isdir(devstack_dir):
        clone_devstack(home)
    create_localrc(localrc_path, log_path, reclone=do_reclone)
    patch_ipv6_devstack(devstack_dir)
    run_devstack(devstack_dir)
    patch_ipv6_radvd_neutron()
    do_restack(devstack_dir)
    # Comment out next 3 lines. Currently no bugs to temporarily patch around.
    #patch_neutron_bugs()
    #restart_neutron_processes()
    #time.sleep(5)
    passed = run_tempest_tests()
    print 'TEMPEST %s' % 'PASSED!' if passed else 'FAILED'
    #cleanup_current_devstack(devstack_dir)
    print 'Done'
    print_date()
    sys.exit(0 if passed else 1)

def cleanup_previous_devstack(devstack_dir):
    print_banner('Clean up previous DevStack instance')
    cleanup_devstack(devstack_dir)

def cleanup_current_devstack(devstack_dir):
    print_banner('    Clean up DevStack instance     ')
    cleanup_devstack(devstack_dir)

def cleanup_devstack(devstack_dir):
    if os.path.isdir(devstack_dir):
        os.chdir(devstack_dir)
        run_cmd_line('./unstack.sh', check_result=False)
    for project in cleanup_kill_projects:
        run_cmd_line('pkill -f %s' % project, check_result=False)
    run_cmd_line('sudo rm %s' % cleanup_dpkg_lock, check_result=False)
    run_cmd_line('sudo rm %s' % cleanup_libvirt_log, check_result=False)
    if do_reclone:
        remove_subdir('/opt')
        #remove_subdir(devstack_dir)

def clone_devstack(home):
    print_banner('         Cloning DevStack          ')
    os.chdir(home)
    run_cmd_line('git clone %s' % devstack_repo)

def create_localrc(localrc_path, log_path, reclone):
    print_banner('  Create localrc for Cisco plugin  ')
    if reclone:
        reclone_flags = do_reclone_flags
    else:
        reclone_flags = no_reclone_flags
    localrc = localrc_tempest % (log_path, log_path) + reclone_flags 
    f = open(localrc_path, 'w')
    f.write(localrc)
    print localrc

def patch_ipv6_devstack(devstack_dir):
    print_banner(" Applying Robert's DevStack Patch  ")
    os.chdir(devstack_dir)
    output, rc = run_cmd_line('git review -d 87987')
    print output

def run_devstack(devstack_dir):
    print_banner('         Running DevStack          ')
    os.chdir(devstack_dir)
    output, stack_rc = run_cmd_line('./stack.sh', check_result=False)
    if stack_rc:
        print 'stack.sh FAILED'
        print_date()
        sys.exit(stack_rc)

def do_restack(devstack_dir):
    print_banner('    Re-Stacking (unstack/stack)    ')
    os.chdir(devstack_dir)
    run_cmd_line('./unstack.sh', check_result=False)
    time.sleep(3)
    output, stack_rc = run_cmd_line('./stack.sh', check_result=False)
    if stack_rc:
        print 'stack.sh FAILED'
        print_date()
        sys.exit(stack_rc)

def patch_ipv6_radvd_neutron():
    print_banner('   Applying RADVD Neutron Patch    ')
    os.chdir(neutron_dir)
    output, rc = run_cmd_line('git review -d 102648')
    print output

def remove_subdir(subdir):
    run_cmd_line('sudo rm -rf %s' % subdir, check_result=False)

def patch_neutron_bugs():
    print_banner('   Applying Temp Neutron Patches   ')
    output, rc = run_cmd_line(neutron_patch_script, check_result=False)
    print output

def restart_neutron_processes():
    print_banner('    Restarting Neutron Processes   ')
    reg_exes = {}
    for proc in neutron_restart_procs:
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
                 out, rc = run_cmd_line('kill -9 %d' %
                                        int(result.group('pid')),
                                        check_result=False)
                 # Re-run the  process if kill was successful
                 if not rc:
                     filename = os.path.join(log_prefix + '-' + proc + '.log')
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

def run_cmd_line(cmd_str, stderr=None, shell=False,
                 echo_cmd=True, check_result=True):
    if echo_cmd:
        print cmd_str
    if shell:
        cmd_args = cmd_str
    else:
        cmd_args = cmd_str.split()
    output = None
    returncode = 0
    try:
        output = subprocess.check_output(cmd_args, shell=shell, stderr=stderr)
    except subprocess.CalledProcessError as e:
        if check_result:
            print e
            sys.exit(e.returncode)
        else:
            returncode = e.returncode
    return output, returncode

def run_tempest_tests():
    print_banner('       Running Tempest Tests       ')
    os.chdir(tempest_dir)
    if not os.path.isdir('.testrepository'):
        run_cmd_line('testr init', check_result=False)
    logfile = os.path.join(log_prefix + '_tempest_log.txt')
    print 'Tests to be run:'
    output, rc = run_cmd_line('cat %s' % test_list_file, check_result=False)
    print output
    cmd = 'testr run --load-list=%s > %s' % (test_list_file, logfile)
    print cmd
    result = os.system(cmd)
    return result == 0

if __name__ == '__main__':
    run_devstack_and_tempest()

