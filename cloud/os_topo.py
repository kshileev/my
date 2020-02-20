def main():
    from cloud.cloud_cfg import CloudCfg
    from cloud.cloud_net import CloudNets

    os = CloudCfg.from_etc_cfg_yaml('k1-4')
    nets = os.nets()
    nets.list()
    pass


if __name__ == '__main__':
    main()

'''


'''