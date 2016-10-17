import threading

from status import WorkerStatus
from worker import Worker


class ScaleHub(object):
    def __init__(self, config):
        """
        type config: dict
        """
        self.workers_config = config['workers']
        self.workers = []
        for worker_config in self.workers_config:
            self.workers.append(Worker(worker_config))

    def go(self):
        self.init_workers()
        self.start_test()

    def is_test_completed(self):
        return reduce(
            lambda prev, curr: prev and (curr.endless or curr.status() == WorkerStatus.test_completed),  # noqa
            self.workers,
            True
        )

    def init_workers(self):
        for worker in self.workers:
            threading.Thread(target=worker.init).start()

        running_workers = range(0, len(self.workers))
        while len(running_workers) > 0:
            for i in running_workers:
                if self.workers[i].status() == WorkerStatus.init_completed:
                    running_workers.remove(i)

    def start_test(self):
        for worker in sorted(self.workers, key=lambda x: x.run_priority):
            threading.Thread(target=worker.start_test).start()

    def stop_endless(self):
        for worker in self.workers:
            if worker.endless:
                worker.stop_test()

    def collect_results(self):
        results = {}
        for worker in self.workers:
            results[worker.id] = worker.collect_results()
        return results
