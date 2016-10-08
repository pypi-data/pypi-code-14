import json

data = None


def data_prepare():
    import MySQLdb
    con = MySQLdb.connect(user="root", passwd="19920819xy", db="reactome")
    cursor = con.cursor()
    cursor.execute("select DB_ID, representedInstance from Vertex")
    f = cursor.fetchall()
    # to int
    return [(int(x[0]), int(x[1])) for x in f]


def compress(data):
    data = sorted(data, key=lambda x: x[0])
    first_dif = [data[0]]
    print data[0:10]
    for i, x in enumerate(data[1:]):
        first_dif.append((x[0] - data[i][0], x[1] - data[i][1]))
    print max([x[0] for x in first_dif[1:]])
    with open("data_folder/raw.json", "w") as fp:
        fp.write(json.dumps(data))


def vertex2id(v):
    global data
    if not data:
        with open("/Users/sheep/pathway/ipy/lib/python2.7/site-packages/pypath/core/ReactomeCustome/data_folder/raw.json") as fp:
            con = json.loads(fp.read())
        data = {x[0]: x[1] for x in con}
    return data.get(int(v))


# if __name__ == '__main__':
    # compress(data_prepare())
    # print vertex2id("10497522")
