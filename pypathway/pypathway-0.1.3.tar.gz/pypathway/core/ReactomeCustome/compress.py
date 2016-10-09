import json
import os

data = None


def compress(data):
    data = sorted(data, key=lambda x: x[0])
    first_dif = [data[0]]
    print(data[0:10])
    for i, x in enumerate(data[1:]):
        first_dif.append((x[0] - data[i][0], x[1] - data[i][1]))
    print(max([x[0] for x in first_dif[1:]]))
    with open("data_folder/raw.json", "w") as fp:
        fp.write(json.dumps(data))


def vertex2id(v):
    global data
    if not data:
        with open(os.path.dirname(os.path.abspath(__file__)) + "/data_folder/raw.json") as fp:
            con = json.loads(fp.read())
        data = {x[0]: x[1] for x in con}
    return data.get(int(v))

