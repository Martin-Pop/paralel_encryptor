import logging
import sys

from multiprocessing import Queue
from logging.handlers import QueueListener, QueueHandler

def configure_logger_queue(file_path, suppress_info=False):

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # WARNING +
    file_handler = logging.FileHandler(file_path, encoding="utf-8",mode='a')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    # INFO +
    if not suppress_info:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        handlers = (file_handler, console_handler)
    else:
        handlers = (file_handler,)

    log_queue = Queue()
    listener = QueueListener(log_queue, *handlers, respect_handler_level=True)

    return log_queue, listener

def add_queue_handler_to_root(queue):
    root = logging.getLogger()
    root.setLevel(logging.NOTSET)
    root.addHandler(QueueHandler(queue))