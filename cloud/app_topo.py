def main():
    import argparse
    from cloud.pod import PodCfg

    parser = argparse.ArgumentParser(description='Check/show all about OS cloud and underlaying structure')
    parser.add_argument('spec_path', type=argparse.FileType('r'), help='path to cfg file ')

    args = parser.parse_args()

    pod_cfg = PodCfg.from_cfg_file(stream = args.spec_path)
    pod_cfg.print()


if __name__ == '__main__':
    main()
