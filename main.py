from multiprocessing import Queue, Process
import os

from io_utils.reader import chunk_reader
from encryption.worker_handler import start_workers, stop_workers

def main():

    file_path = 'test.txt'
    chunk_size = 5
    task_queue = Queue()

    reader = Process(target= chunk_reader, args=(file_path, chunk_size, task_queue))
    reader.start()

    worker_count = 4
    key = os.urandom(32)
    base_nonce = int.from_bytes(os.urandom(8), "big")
    result_queue, workers = start_workers(worker_count, task_queue, key, base_nonce)

    reader.join()
    stop_workers(worker_count, task_queue)

    #fix deadlock by implementing writer
    for worker in workers:
        print('joining worker')
        worker.join()

    print('end')

if __name__ == "__main__":
    main()
