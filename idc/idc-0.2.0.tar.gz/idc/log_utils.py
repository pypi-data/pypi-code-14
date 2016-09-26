import logging
import config
import os


def set_log():

    log_path = config.Config().get_path_exp('log_path')
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    file_handler = logging.FileHandler(
        filename=os.path.join(
            os.path.realpath(log_path),
            'idc.log'
        )
    )

    file_formatter = logging.Formatter(
        fmt=(
            '%(asctime)s::%(filename)s::%(funcName)s::%(lineno)s::'
            '%(name)s::%(levelname)s::%(message)s'
        )
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter('%(asctime)s - %(message)s')

    stream_handler.setFormatter(stream_formatter)

    logging.root.handlers = [file_handler, stream_handler]
    logging.root.setLevel(logging.DEBUG)

