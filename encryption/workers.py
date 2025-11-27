from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from io_utils.reader import map_read_file
from io_utils.writer import map_write_file

def worker(in_file, out_file, task_queue, chunk_size, key, base_nonce, encrypt, stop_token=None):
    """
    Worker that is run in a process
    :param in_file: input file path
    :param out_file: output file path
    :param task_queue: queue containing tasks (read offsets)
    :param chunk_size: size of a chunk
    :param key: encryption key
    :param base_nonce: base nonce used for encryption
    :param encrypt: encryption flag
    :param stop_token: token that stops workers
    """

    file_in, mm_in = map_read_file(in_file)
    file_out, mm_out = map_write_file(out_file)

    aes = AESGCM(key)
    cipher_function = aes.encrypt if encrypt else aes.decrypt

    if encrypt:
        input_header_size = 0
        input_step = chunk_size

        output_header_size = 12
        output_step = chunk_size + 16
    else:
        input_header_size = 12
        input_step = chunk_size + 16

        output_header_size = 0
        output_step = chunk_size

    try:
        while True:
            task = task_queue.get()

            if task == stop_token:
                break

            read_offset, chunk_length = task
            chunk_id = (read_offset - input_header_size) // input_step
            chunk_data = mm_in[read_offset: read_offset + chunk_length]

            nonce_int = (base_nonce << 32) | chunk_id
            nonce = nonce_int.to_bytes(12, 'big')

            out_data = cipher_function(nonce, chunk_data, None)

            write_offset = output_header_size + (chunk_id * output_step)
            out_len = len(out_data)
            mm_out[write_offset: write_offset + out_len] = out_data


    except Exception as e:
        print('Unexpected error:', e)
    finally:
        mm_in.close()
        mm_out.close()
        file_in.close()
        file_out.close()
