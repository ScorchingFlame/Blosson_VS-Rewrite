import sqlite3, json

conn1 = sqlite3.connect("../data/voter.db")
conn2 = sqlite3.connect("../data/voting.db")

adnumber = input("Enter the admission number you want to get the details of: ")
idk = int(adnumber)

curson1 = conn2.cursor()
cursor2 = conn1.cursor()
if curson1.execute(f"SELECT * FROM voters WHERE adnumber = {idk}").fetchone() is not None:
    if curson1.execute(f"SELECT * FROM voters WHERE adnumber = {idk}").fetchone()[4] == 1:
        # print(cursor2.execute(f"SELECT * FROM votingtowho WHERE adnumber = {idk}").fetchone()[1])
        array = json.loads(cursor2.execute(f"SELECT * FROM votingtowho WHERE adnumber = {idk}").fetchone()[1])
        for k in array:
            candidate = curson1.execute(f"SELECT * FROM candidates WHERE id = {array[k]}").fetchone()
            position_name = curson1.execute(f"SELECT * FROM positions WHERE id = {candidate[5]}").fetchone()[1]
            print(f"{position_name} : {candidate[1]}")
    else:
        print("ERROR: The person did not vote yet")
else:
    print("ERROR: The person does not exist")

input("Press Enter to exit")