import paramiko
import unittest

ip, username, password = '172.28.121.187', 'admin', 'Lab1234!'


class TestParamiko(unittest.TestCase):
    def test_client_init(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(policy=paramiko.AutoAddPolicy)
        ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
        print(ssh_client.exec_command('show version'))

