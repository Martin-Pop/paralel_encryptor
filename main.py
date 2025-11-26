from multiprocessing import Queue, Process
import os

from console.args import parse_args
from utils.crypto import derive_key_from_string

from io_utils.reader import chunk_reader, read_header
from io_utils.writer import chunk_writer
from encryption.worker_handler import start_workers, stop_workers

def main():

    #header: 8b - nonce, 4b - chunk size
    task_queue = Queue()

    #read
    reader = Process(
        target= chunk_reader,
        args=(in_file_path, chunk_size, task_queue, is_encryption)
    )
    reader.start()

    #work
    result_queue, workers = start_workers(worker_count, task_queue, key, nonce, is_encryption, None)

    #write
    writer = Process(
        target= chunk_writer,
        args=(out_file_path, result_queue, is_encryption ,nonce.to_bytes(8,'big') + chunk_size.to_bytes(4,'big'), None)
    )
    writer.start()

    #stop
    reader.join()
    stop_workers(worker_count, task_queue)

    result_queue.put(None)
    writer.join()
    # print('writer end')

    for worker in workers:
        # print('joining worker')
        worker.join()

if __name__ == "__main__":

    args = parse_args()

    is_encryption = args.encrypt
    in_file_path = args.input
    out_file_path = args.output
    chunk_size = args.chunk_size
    worker_count = args.workers
    key = derive_key_from_string(args.key)

    if is_encryption:
        nonce = int.from_bytes(os.urandom(8), "big")
        chunk_size = args.chunk_size
    else:
        header = read_header(in_file_path)
        nonce = int.from_bytes(header[0], "big")
        chunk_size = int.from_bytes(header[1], "big")

    print("MODE:", "ENCRYPT" if is_encryption else "DECRYPT")
    print("IN:", in_file_path)
    print("OUT:", out_file_path)
    print("CHUNK:", chunk_size)
    print("WORKERS:", worker_count)
    print("KEY:", args.key)

    main()
