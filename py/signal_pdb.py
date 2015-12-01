from optparse import OptionParser


def signal_handler_for_pdb(signum, stack):
    import pdb

    pdb.Pdb().set_trace(frame=stack)


def configure_pdb():
    import signal
    import os

    signal.signal(signal.SIGUSR1, signal_handler_for_pdb)
    print 'To start debugging use: sudo kill -SIGUSR1 {0}'.format(os.getpid())


def main():
    import time

    while True:
        print 'sleeping....'
        time.sleep(30)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--with-pdb", dest="is_with_pdb", action="store_true")
    (options, args) = parser.parse_args()
    if options.is_with_pdb:
        configure_pdb()
    main()
