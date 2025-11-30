from multiprocessing import Process
from .workers import encryption_worker

def start_workers(worker_count, config):

    workers = []
    for _ in range(worker_count):
        process = Process(target=encryption_worker, args=(config,))
        workers.append(process)

        process.start()

    return workers

