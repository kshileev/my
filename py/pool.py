def f(item):
    func = item.pop['function']
    queue = item.pop['queue']
    func(queue)


def monitor(queue):
    import time
    is_scenario_finished = False

    while not is_scenario_finished:
        is_scenario_finished = queue.get_nowait()
        print 'monitoring... ',
        time.sleep(1)


def scenario(queue):
    import time

    print 'doing scenario'
    time.sleep(10)
    queue.put_nowait('SCENARIO_FINISHED')


def main():
    import multiprocessing

    q = multiprocessing.Queue()

    try:
        a = q.get_nowait()
    except multiprocessing.Queue.Empty:
        pass
    q.put_nowait('AAAA')
    a = q.get_nowait()
    values = [{'function': monitor, 'queue': q},
              {'function': scenario, 'queue': q}]
    p = multiprocessing.Pool(processes=len(values))
    p.map(f, values)


if __name__ == '__main__':
    main()
