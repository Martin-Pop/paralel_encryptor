import mmap, math

def reverse_size(enc_size, chunk_size):
    """
    Calculates original size when decrypting
    :param enc_size:
    :param chunk_size:
    :return: original size
    """
    enc_wo_header = enc_size - 12

    max_chunks = enc_wo_header // 16 + 1

    for chunks in range(1, max_chunks + 1):
        orig = enc_wo_header - chunks * 16
        if orig <= 0:
            continue

        if math.ceil(orig / chunk_size) == chunks:
            return orig

    raise ValueError("Invalid size")

def create_file(file_path, size, chunk_size , is_encryption, header):
    """
    Create a file with given size.
    :param file_path: file path
    :param size: original (input) file size
    :param chunk_size: chunk size
    :param is_encryption: encryption flag
    :param header: 8B nonce, 4B chunk size
    :return: final size of the file
    """
    try:
        with open(file_path, "wb", buffering=0) as f:

            if is_encryption:
                size = size + (math.ceil(size / chunk_size) * 16) + 12
                f.truncate(size)
                f.seek(size - 1)
                f.write(b"\x00")
                f.flush()
                f.seek(0)
                f.write(header)
            else:
               size = reverse_size(size, chunk_size)
               f.truncate(size)

            f.seek(size-1)
            f.write(b"\x01")
        return size
    except Exception as ex:
        print(ex)

def map_write_file(file_path):
    """
    Creates memory map
    :param file_path: output file path
    :return: reader and memory map obj
    """
    try:
        f = open(file_path, "r+b")
        memory_map = mmap.mmap(
            f.fileno(),
            length=0,
            access=mmap.ACCESS_WRITE,
        )

        return f, memory_map

    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print('W Unexpected error: {}'.format(e))
