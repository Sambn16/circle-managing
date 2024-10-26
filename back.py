import sqlite3


def connect():
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS friends (id INTEGER PRIMARY KEY, fullname TEXT, age INTEGER, phone INTEGER, location TEXT)'
    )
    conn.commit()
    conn.close()


def insert(fullname, age, phone, location):
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO friends VALUES (NULL, ?,?,?,?)", (fullname, age, phone, location))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM friends")
    rows = cur.fetchall()
    conn.close()
    return rows


def search(fullname):
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM friends WHERE fullname LIKE ?", ('%' + fullname + '%',))
    rows = cur.fetchall()
    conn.close()
    return rows


def remove(id):
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM friends WHERE id=?", (id,))
    conn.commit()
    conn.close()


def edit(id, fullname, age, phone, location):
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute("UPDATE friends SET fullname=?, age=?, phone=?, location=? WHERE id=?", (fullname, age, phone, location, id))
    conn.commit()
    conn.close()



connect()
# insert("sam mousavi", 19, +989305580325, "Karaj, Iran")
# insert("mobin amiri", 19, 123, "Tehran, Iran")
# insert("roxana ashoori", 18, +989116209402, "Rasht, Iran")
# insert("mehdi farhani", 20, +321, "Tehran, Iran")
# insert("mehdi madani", 19, +231, "Abadan, Iran")
# insert("devan", 20, +132, "Mashhad, Iran")


# print(search("sam"))