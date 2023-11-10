import sqlite3 as sql

con = sql.connect('ratings.db')

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS log")

sql = '''CREATE TABLE "log" (
        "logId" INTEGER PRIMARY KEY AUTOINCREMENT,
        "parkName" TEXT NOT NULL,
        "state" TEXT NOT NULL,
        "yearVisited" INTEGER NOT NULL,
        "rating" REAL NOT NULL,
        "comments" TEXT NOT NULL
)'''

cur.execute(sql)

con.commit()

con.close()