import os, time

from console.args import parse_args
from utils.crypto import derive_key_from_string

from io_utils.reader import read_header,get_file_size
from io_utils.writer import create_file
from encryption.chunker import create_chunk_task_queue

from encryption.worker_handler import start_workers

def main():

    #header: 8b - nonce, 4b - chunk size
    start = time.perf_counter()

    file_size_in = get_file_size(in_file_path)
    create_file(out_file_path, file_size_in, chunk_size, is_encryption,nonce.to_bytes(8, 'big') + chunk_size.to_bytes(4, 'big'))

    task_queue = create_chunk_task_queue(chunk_size, file_size_in, is_encryption)

    for i in range(worker_count):
        task_queue.put(None)

    workers = start_workers(in_file_path, out_file_path, worker_count, task_queue, chunk_size, key, nonce, is_encryption, None)
    for w in workers:
        w.join()

    end = time.perf_counter()

    elapsed_ms = (end - start) * 1000
    print(f"DONE IN: {elapsed_ms:.3f} ms")

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
