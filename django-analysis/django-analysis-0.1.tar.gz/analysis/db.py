import os
import sqlite3


def init_db():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'analysis.db'))
    conn.execute(
        '''CREATE TABLE "analysis_request" ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
"view_func_path" VARCHAR(100) NOT NULL,
"url" VARCHAR(100) NOT NULL,
"method" VARCHAR(10) NOT NULL,
"date" DATETIME NOT NULL,
"sql_times" INTEGER NOT NULL,
"sql_used" DECIMAL NOT NULL,
"request_used" DECIMAL NOT NULL);
''')
    conn.execute(
        '''CREATE TABLE "analysis_sqlentry" ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
"db" VARCHAR(50) NOT NULL,
"sql" TEXT NOT NULL,
"time" DECIMAL NOT NULL,
"request_id" INTEGER NOT NULL REFERENCES "analysis_request" ("id"));''')
    conn.execute('''CREATE INDEX "analysis_sqlentry_f68d2c36" ON "analysis_sqlentry" ("request_id");''')
    conn.close()
