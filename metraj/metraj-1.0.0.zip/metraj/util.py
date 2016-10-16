
import pandas as pd
from sqlalchemy import create_engine


def sqlite2frame(source, table, dest):
    # Sqlite connect
    conn = create_engine('sqlite:///{}'.format(source))
    data = pd.read_sql_table(table, conn)
    data.to_csv(dest)


if __name__ == "__main__":
    FILE_IN = None
    FILE_OUT = None
    TABLE = "LOCALIZATIONS"
    sqlite2frame(FILE_IN, TABLE, FILE_OUT)
