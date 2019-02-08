from multiprocessing import Process, Queue


class TaskQueue:

    def __init__(self, task):
        self.queue = Queue()
        self.p = Process(target=self._reader, args=(task,))
        self.p.daemon = True

    def _reader(self, task):
        while True:
            args, kwargs = self.queue.get()
            task(*args, **kwargs)

    def push(self, *args, **kwargs):
        self.queue.put((args, kwargs))

    def start(self):
        self.p.start()

    def stop(self):
        self.p.close()
