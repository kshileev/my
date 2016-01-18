import time
import log
import decorators


def fun(n):
    while n > 0:
        n -= 1

@decorators.print_time
def sequencial(function, args):
    map(function, args)


@decorators.print_time
def multi_processes(function, args):
    import multiprocessing

    p = multiprocessing.Pool(processes=len(args))
    p.map(func=function, iterable=args)


@decorators.print_time
def multi_threads(function, args):
    import threading

    threads = [threading.Thread(target=function, args=(x, )) for x in args]
    map(lambda thread: thread.start(), threads)
    map(lambda thread: thread.join(), threads)


@decorators.print_time
def multi_forks(function, args):
    import os
    import sys
    from log import create_logger

    pids = []

    def fork_new_process(value):
        try:
            pid = os.fork()
        except AttributeError:
            logger = create_logger()
            logger.error('Failed to fork subprocess')
        else:
            if pid > 0:
                pids.append(pid)
            else:
                function(value)
                sys.exit(0)

    map(fork_new_process, args)


def main():
    import multiprocessing

    start_n = 100000000
    n_procs = 2

    logger = log.create_logger()
    logger.warning('N cpu = {0}'.format(multiprocessing.cpu_count()))

    multi_forks(function=fun, args=n_procs*[start_n])
    sequencial(function=fun, args=n_procs*[start_n])
    multi_processes(function=fun, args=n_procs*[start_n])
    multi_threads(function=fun, args=n_procs*[start_n])

    lst = [multiprocessing.Process(target=monitor),
           multiprocessing.Process(target=activity),
           multiprocessing.Process(target=disturbance)]

    map(lambda x: x.start(), lst)
    map(lambda x: x.join(), lst)


if __name__ == '__main__':
    main()
