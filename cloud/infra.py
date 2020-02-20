def main():
    import argparse
    import yaml
    import os
    from cloud.cimc import Cimcs
    from cloud.server import ServerCfg


    parser = argparse.ArgumentParser(description='Check given TB spec file')
    parser.add_argument('spec_path', type=argparse.FileType('r'), help='path to setup_data file ')

    args = parser.parse_args()

    spec_d = yaml.safe_load(args.spec_path)

    pod_name = os.path.basename(args.spec_path.name).replace('.spec', '')
    mgm = ServerCfg(name=f'{pod_name}.mgm', ip=spec_d['mgm']['ip6'], uname=spec_d['mgm']['uname'], passwd=spec_d['mgm']['passwd']).create_server()
    cimcs = Cimcs.from_spec_d(cimc_spec=spec_d['cimc'], proxy_srv=mgm)
    cimcs.verify_all_parameters()

if __name__ == '__main__':
    main()