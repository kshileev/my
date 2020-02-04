def main():
    import argparse
    import os
    from ats.easypy import run

    parser = argparse.ArgumentParser(description='OS pod topo')
    parser.add_argument('--is_with_switches', type=bool, default=True, help='try to get switches info')

    args = parser.parse_known_args()

    is_with_switches = args[0].is_with_switches

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    run(testscript=os.path.join(repo, 'CCP', 'ccp_create_cluster.py'), is_with_switches=is_with_switches, taskid='POD TOPO')
