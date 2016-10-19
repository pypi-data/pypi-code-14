import logging
import hashlib

def process_log_message(message, session_key):
    for entry in message:
        entry['session_key'] = hashlib.md5(session_key).hexdigest()
        write_log(entry['logger'], entry)


def write_log(log_name, entry):
    logger = logging.getLogger(log_name)
    logger.info(entry)


