import sqlite3

conn= sqlite3.connect("database.db")
c= conn.cursor()
c.execute("IF NOT EXIST CREATE TABLE attendance(candidate_id, time)")
conn.close()

def add_to_db(data):
    conn= sqlite3.connect("database.db")
    c= conn.cursor()
    c.execute("INSERT INTO atttendance VALUES(?, ?)", (data["Name"], data["Entry_Time"]))
    conn.commit()
    conn.close()

def visualise_data():
    conn= sqlite3.connect("database.db")
    c= conn.cursor()
    data= c.execute("SELECT * FROM attendance")
    conn.close()

    for row in data:
        print(row)
    