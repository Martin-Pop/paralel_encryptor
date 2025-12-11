from multiprocessing import Process
from .workers import encryption_worker

import logging
logger = logging.getLogger(__name__)

def start_workers(worker_count, config):
    """
    Starts encryption workers (processes)
    :param worker_count: how many workers
    :param config: worker configuration
    :return: list of workers
    """
    workers = []
    try:
        for _ in range(worker_count):
            process = Process(target=encryption_worker, args=(config,))
            workers.append(process)

            process.start()

    except Exception as e:
        logger.error(f'Failed to start encryption workers {e}', exc_info=True)
        for process in workers:
            process.terminate()

    return workers