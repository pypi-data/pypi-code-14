import MySQLdb


def connect():
    con = MySQLdb.connect(host="10.104.146.158", db="analyse", passwd="19920819xy", user="root")
    cursor = con.cursor()
    return con, cursor


def query(pathway):
    con, cursor = connect()
    cursor.execute("select * from kegg_gene left join kegg_data on kegg_gene.id=kegg_data.id where pathway=\"{}\";".format(pathway))
    result = {}
    for x in cursor.fetchall():
        if x[5]:
            result[x[0]] = [x[5: 12],
                            x[12: 19],
                            x[19: 26],
                            x[26: 33]]
    return result


# if __name__ == '__main__':
#     print query("ko04610")