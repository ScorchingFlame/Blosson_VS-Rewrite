import xlsxwriter
import sqlite3
t = 0
def eren():
    global t
    t = t + 1
    return t
conn = sqlite3.connect("../data/voting.db")

workbook = xlsxwriter.Workbook('result.xlsx')

for x in conn.execute("SELECT * FROM positions"):
    sheet = workbook.add_worksheet(x[1].replace(" ", ""))
    sheet.write("A1", "id")
    sheet.write("B1", "name")
    sheet.write ("C1", "STD")
    sheet.write ("D1", "House")
    sheet.write ("E1", "Position")
    sheet.write ("F1", "Votes")
    w = 2
    for i in conn.execute(f"SELECT * FROM candidates WHERE Position={x[0]} ORDER BY Votes desc").fetchall():
        sheet.write(f"A{w}", f"{i[0]}")
        sheet.write(f"B{w}", f"{i[1]}")
        sheet.write(f"C{w}", f"{i[2]}")
        sheet.write(f"D{w}", f"{i[3]}")
        sheet.write(f"E{w}", f"{i[5]}")
        sheet.write(f"F{w}", f"{i[6]}")
        w = w+1

workbook.close()
input("Click enter to exit")
