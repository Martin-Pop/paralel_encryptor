from multiprocessing import Process
from .workers import worker

def start_workers(in_file, out_file,worker_count,task_queue, chunk_size, key, base_nonce, encrypt ,stop_token=None):
    """
    Starts workers
    :param in_file: input file path
    :param out_file: output file path
    :param worker_count: number of workers
    :param task_queue: queue containing tasks (read offsets)
    :param chunk_size: size of a chunk
    :param key: encryption key
    :param base_nonce: base nonce used for encryption
    :param encrypt: encryption flag
    :param stop_token: token that stops workers
    :return: list of workers
    """
    workers = []
    for _ in range(worker_count):
        process = Process(target=worker, args=(in_file, out_file,task_queue,chunk_size, key, base_nonce, encrypt ,stop_token))
        workers.append(process)

        process.start()

    return workers

