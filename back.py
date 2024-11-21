import sqlite3


def connect():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY,
                                      chat_id INTEGER,
                                      name TEXT,
                                      birthday INTEGER)
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Friends (id INTEGER PRIMARY KEY,
                                        fullname TEXT,
                                        nickname TEXT,
                                        birthday INTEGER,
                                        phone INTEGER,
                                        location TEXT,
                                        friend_of INTEGER NOT NULL,
                                        FOREIGN KEY(friend_of) REFERENCES Users(chat_id))
        """)
    
    conn.commit()
    conn.close()


def user_data_insert(chat_id, name, birthday=0000-00-00):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Users VALUES (NULL, ?,?,?)", (chat_id, name, birthday))
    conn.commit()
    conn.close()


def user_data_view(chat_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE chat_id=?", (chat_id,))
    result = cur.fetchall()
    conn.close()
    return result


# ======================== FRIENDS SECTION ============================


def insert(fullname, nickname, birthday, phone, location, friend_of):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO friends VALUES (NULL, ?,?,?,?,?,?)", (fullname, nickname, birthday, phone, location, friend_of))
    conn.commit()
    conn.close()


def view(chat_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Friends WHERE friend_of=?", (chat_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def search(fullname):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM friends WHERE fullname LIKE ?", ('%' + fullname + '%',))
    rows = cur.fetchall()
    conn.close()
    return rows


def remove(fullname):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Friends WHERE fullname=?", (fullname,))
    conn.commit()
    conn.close()


def edit(fullname, nickname, birthday, phone, location, old_fullname):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("UPDATE Friends SET fullname=?, nickname=?, birthday=?, phone=?, location=? WHERE fullname=?", (fullname, nickname, birthday, phone, location, old_fullname))
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