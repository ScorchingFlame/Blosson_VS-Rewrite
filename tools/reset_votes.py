import sqlite3

conn = sqlite3.connect('../data/voting.db')

l = input("You Sure You Want to reset the votes? y/n : ")

if l == "y":
    conn.execute("UPDATE candidates SET Votes = 0")
    conn.commit()