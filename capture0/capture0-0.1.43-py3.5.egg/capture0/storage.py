import datetime
import json
import logging
import os
import pprint
import uuid
from typing import Mapping, List

import pytz as pytz
from capture0.config import CONFIG

log = logging.getLogger(__name__)

def store_data(dataset: str, record: Mapping):
    record = dict(**record)
    log.info("Writing data: %s" % pprint.pformat(record))

    id = str(uuid.uuid1())
    dataset_dir = os.path.join(CONFIG["SAVE_DIR"], dataset)
    record["uuid"] = id
    record["timestamp"] = datetime.datetime.now(tz=pytz.utc).isoformat(" ")

    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    file_path = os.path.join(dataset_dir, "%s.json" % id)

    with open(file_path, "w") as output_file:
        output_file.write(json.dumps(record, sort_keys=True, indent=4))
        log.info("Saved %s" % file_path)


def unpack_list(v):
    if isinstance(v, list):
        return ";".join(v)
    return v


def filter_column(k):
    if k in ["csrf_token"]:
        return False
    return True


def build_report(dataset: str) -> List[Mapping]:
    data_directory = os.path.join(CONFIG["SAVE_DIR"], dataset)
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            filepath = os.path.join(data_directory, filename)

            with open(filepath) as datafile:
                try:
                    data = json.load(datafile)
                except json.JSONDecodeError:
                    log.warn("%s is corrupted" % filepath)
                    continue

                try:
                    yield {k: unpack_list(v) for k, v in data.items() if filter_column(k)}
                except (AttributeError, RuntimeError):
                    log.warn("%s is defective" % filepath)
                    continue
