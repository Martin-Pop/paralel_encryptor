import os, mmap

def read_header(file_path):
    """
    Reads header from file
    :param file_path: path to file
    :return: Header (8B nonce + 4B chunk size) 12B or None
    """
    try:
        with open(file_path, 'rb') as f:
            base_nonce_bytes = f.read(8)
            chunk_size = f.read(4)

            return base_nonce_bytes, chunk_size
    except FileNotFoundError:
        print('File not found')
        return None
    except Exception as e:
        print('Unexpected error: {}'.format(e))
        return None

def map_read_file(file_path):
    """
    Creates memory map
    :param file_path: input file path
    :return: reader and memory map obj
    """
    try:
        f = open(file_path, 'rb')
        memory_map = mmap.mmap(f.fileno(), 0, tagname=None, access=mmap.ACCESS_READ)
        return f, memory_map

    except Exception as e:
        print('Unexpected error: {}'.format(e))

def get_file_size(file_path):
    """
    Gets size of a file
    :param file_path: paht of the file
    :return: size
    """
    try:
      with open(file_path, 'rb') as f:
          f.seek(0, os.SEEK_END)
          file_size = f.tell()
          return file_size

    except Exception as e:
        print('Unexpected error: {}'.format(e))
