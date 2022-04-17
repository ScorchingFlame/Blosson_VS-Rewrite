@app.route('/upload/vexcel', methods=['POST'])
def uexcel():
    file = request.files['file'].read()
    try:
        fh = FileHandler()
        fh.write_into(file)
        # print(fh.file.name)
        # # sleep(60)
        loc = (fh.file.name)
        a : xlrd.Book = xlrd.open_workbook(loc)
        sheet = a.sheet_by_index(0)
        sheet.cell_value(0,0)

        if not sheet.row_values(0) == ["AdmissionNumber", "Name", "STD", "House"]:
            # socketio.emit('sleeep', {'done': 'ok'})
            return abort(500)

        # k = [int, str, int, Literal["WINTER", "SUMMER", "SPRING"]]
        # sleep(60)
        tp = []
        for i in range(1, sheet.nrows-1):
            meh = [x if type(x) == str else int(x) for x in sheet.row_values(i)]
            meh.append(0)
            tp.append(tuple(meh))

        cur = conn.cursor()
        cur.executemany("INSERT INTO voters VALUES (?, ?, ?, ?, ?)", tp)
        conn.commit()
        cur.close()
        return "Ok"
    except Exception as e:
        # socketio.emit('sleeep', {'done': 'ok', 'error': e})
        return abort(500)
