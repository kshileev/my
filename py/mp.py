class Worker:
    def __init__(self, n, pipe):
        self.name = 'worker{}'.format(n)
        self.pipe = pipe

    def loop(self):


def main():
    import multiprocessing

    pipe = multiprocessing.Pipe()
    workers = [Worker(n=i, pipe=pipe.) for i in range(1,4)]

    with multiprocessing.Pool(len(workers)) as pool:
        results = pool.map()

if __name__ == '__main__':
    main()