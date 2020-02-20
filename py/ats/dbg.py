class TestCfgServer(object):
    def __init__(self, d):
        self.__dict__.update(d)


class TestCfgServers(object):
    def __init__(self, d):
        self.build_node = TestCfgServer(d['build_node'])


class TestCfg(object):
    def __init__(self, d):
        import yaml

        d = yaml.safe_load(d)
        self.name = d['testbed']['name']
        self.servers = TestCfgServers(d['testbed']['servers'])


def dbg():
    import argparse
    import importlib.util
    import os
    import sys

    repo = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def cfg(value):
        if not value.startswith('CFG.'):
            value = f'CFG.{value}'
        if not value.endswith('.yaml'):
            value = f'{value}.yaml'
        etc = os.path.join(repo, 'etc')
        try:
            with open(os.path.join(etc, value)) as f:
                return TestCfg(f.read())
        except FileNotFoundError:
            raise argparse.ArgumentTypeError(f'{value} is not in {etc}')

    def run(value):
        py = value if value.endswith('.py') else f'{value}.py'
        job_fld = os.path.join(repo, 'py')
        mod_path = os.path.join(job_fld, 'os', py)
        if os.path.isfile(mod_path):
            mod_spec = importlib.util.spec_from_file_location(value, mod_path)
            mod = importlib.util.module_from_spec(mod_spec)
            mod_spec.loader.exec_module(mod)
            print(dir(mod))
            return value
        else:
            raise argparse.ArgumentTypeError(f'{py} is not in {job_fld}')

    parser = argparse.ArgumentParser()
    parser.add_argument('cfg', type=cfg, help='one of $REPO/etc/CFG.XXX.yaml files')
    parser.add_argument('run', type=run, help='one of $REPO/py/XXX.py files')
    args = parser.parse_known_args()


if __name__ == '__main__':
    dbg()
