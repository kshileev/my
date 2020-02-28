def main():
    import argparse
    from cloud.pod import PodCfg


    parser = argparse.ArgumentParser(description='Check given TB spec file')
    parser.add_argument('spec_path', type=argparse.FileType('r'), help='path to setup_data file ')

    args = parser.parse_args()

    pod = PodCfg.from_yaml_file(stream = args.spec_path).create_pod()
    pod.cimcs.verify_all_parameters()

if __name__ == '__main__':
    main()