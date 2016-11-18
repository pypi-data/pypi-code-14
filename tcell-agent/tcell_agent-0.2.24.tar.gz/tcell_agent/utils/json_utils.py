import json
import logging

LOGGER = logging.getLogger('tcell_agent').getChild(__name__)

def parse_json(json_str):
    if not json_str:
        return None

    try:
        if isinstance(json_str, bytes):
            return json.loads(json_str.decode("utf-8"))
        else:
            return json.loads(json_str)
    except Exception as e:
        LOGGER.error("Error decoding json: {e}".format(e=e))
        LOGGER.debug(e, exc_info=True)
        return None
