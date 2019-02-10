"""
This module contains components to help with data processing.
The only thing that this module exports is the `TaskQueue`.
"""

from multiprocessing import Process, Queue


class TaskQueue:
    """
    This class represents a queue that executes tasks that get pushed to it.
    The execution is performed in a background process.
    """

    def __init__(self, task):
        """
        The parameter `task` expects a function for the task which
        is to be executed when new data is pushed to the queue.
        """
        self.queue = Queue()
        self.p = Process(target=self._reader, args=(task,))
        self.p.daemon = True

    def _reader(self, task):
        while True:
            # The process is blocked until new data is
            # available in the queue.
            args, kwargs = self.queue.get()
            task(*args, **kwargs)

    def push(self, *args, **kwargs):
        """
        Adds a new entry to be processed to the end of the queue.
        This function accepts arguments for the task function
        passed in to the constructor.
        """
        self.queue.put((args, kwargs))

    def start(self):
        """
        Starts the process which executes entries from the queue.
        """
        self.p.start()

    def stop(self):
        """
        Terminates the process which executes entries from the queue.
        This function will not wait for running tasks to finish executing.
        """
        if self.p.is_alive():
            self.p.terminate()
