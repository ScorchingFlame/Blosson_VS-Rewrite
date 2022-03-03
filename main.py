from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
from flask_compress import Compress
from flask_socketio import SocketIO
import flask, sqlite3, socket, asyncio, random, os, re, pandas
from flask import redirect, request, url_for
from flask import Flask, render_template


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

print(get_ip_address())
app = Flask(__name__)
socketio = SocketIO(app,)
compress = Compress()
compress.init_app(app)
conn = sqlite3.connect('data/voting.db')
conn.execute("""CREATE TABLE IF NOT EXISTS positions (
	            id INTEGER PRIMARY KEY,
	            name TEXT NOT NULL,
	            wcs TEXT NOT NULL
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS candidates (
	            id INTEGER PRIMARY KEY,
	            name TEXT NOT NULL,
	            STD TEXT NOT NULL,
                DOB TEXT NOT NULL,
                House TEXT NOT NULL,
                Photo TEXT NOT NULL,
                Position INTEGER NOT NULL,
                Votes INTEGER NOT NULL
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS voters (
                adnumber INTEGER NOT NULL,
                name TEXT NOT NULL,
                STD TEXT NOT NULL,
                DOB TEXT NOT NULL,
                House TEXT NOT NULL
                Voted BOOLEAN NOT NULL
                );""")
                

@app.route('/admin')
def index():
    return render_template('index.html')

@app.route('/admin/positions')
def positions():
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from positions")
    record = cursor.fetchall()
    return render_template('positions.html', tm=record)

@app.route('/admin/positions/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create-position.html', ph="", mode_name="Submit", bck_btn="../positions")
    if request.method == 'POST':
        name = flask.request.values.get('name') # Your form's
        wcs_str = flask.request.values.get('wcs')
        conn.execute(f"INSERT INTO positions (name, wcs) VALUES ('{name}', '{wcs_str}')")
        conn.commit()   
        return redirect('/admin/positions')

@app.route('/admin/positions/edit/<id>', methods=['GET','POST'])
def edit_positions(id: int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from positions where id={str(id)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/positions')
    if request.method == 'GET':
        return render_template('create-position.html', ph= record[1], mode_name="Edit", bck_btn="../../positions")
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from positions where id={str(id)}")
        record = cursor.fetchall()
        name = flask.request.values.get('name') # Your form's
        wcs_str = flask.request.values.get('wcs')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE positions SET name='{name}', wcs='{wcs_str}' WHERE id = {id}")
        conn.commit()
        return redirect('/admin/positions')

@app.route('/admin/positions/delete/<id>')
def delete_positions(id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from positions where id={str(id)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/positions')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from positions where id != {id}")
    record2 = cursor.fetchall()
    rec3 = cursor.execute(f"SELECT * FROM candidates where Position != {id}")
    new_record = []
    new_r_c = []
    for o in record2:
        pl = list(o)
        pl[0] = None
        al = tuple(pl)
        new_record.append(al)
    for o in rec3:
        pl = list(o)
        pl[0] = None
        al = tuple(pl)
        new_r_c.append(al)
    sql_statement = 'INSERT INTO positions VALUES (?, ?, ?)'
    sql_statement_c = 'INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    cur = conn.cursor()
    cur.execute("DELETE FROM positions")
    cur.execute("DELETE FROM candidates")
    cur.executemany(sql_statement, new_record)
    cur.executemany(sql_statement_c, new_r_c)
    conn.commit()
    return redirect('/admin/positions')

@socketio.on('llol')
def lmfo(data):
    print(data)

@app.route('/admin/candidates')
def candidates():
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates")
    record = cursor.fetchall()
    cursor.execute(f"SELECT * FROM positions")
    recordpos = cursor.fetchall()
    new_r = []
    for i in recordpos:
        for u,j in enumerate(record):
            if i[0] == j[6]:
                j = list(j)
                j[6] = i[1]
                new_r.append(tuple(j))
                record.pop(u)
    return render_template('candidates.html', tm=new_r)

@app.route('/admin/candidates/create', methods=['GET', 'POST'])
def createc():
    if request.method == 'GET':
        return render_template('create-candidates.html', ph="", phs=0, mode_name="Create", bck_btn="../candidates", poses=conn.execute('SELECT * from positions').fetchall())
    if request.method == 'POST':
        fola = request.files['photo']
        ffname = f"{''.join(random.choice('0123456789ABCDEFMJWksiwl') for i in range(6))}.{fola.filename.split('.')[-1]}"
        fola.save(f"./static/pics/{ffname}")
        name = flask.request.values.get('name') # Your form's
        std = flask.request.values.get('std')
        date = flask.request.values.get('date')
        date = change_date_format(date)
        house = flask.request.values.get('house')
        pos = flask.request.values.get('pos')
        votes = flask.request.values.get('votes')
        conn.execute(f"INSERT INTO candidates (name, STD, DOB, House, Photo, Position, Votes) VALUES ('{name}', '{std}', '{date}', '{house}', '{ffname}', {pos}, {votes})")
        conn.commit()   
        return redirect('/admin/candidates')


@app.route('/admin/candidates/delete/<id>')
def delete_candidate(id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates where id={str(id)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/candidates')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates where id != {str(id)}")
    record2 = cursor.fetchall()
    os.remove(f'./static/pics/{record[5]}')
    new_record = []
    for o in record2:
        pl = list(o)
        pl[0] = None
        al = tuple(pl)
        new_record.append(al)
    sql_statement = 'INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    cur = conn.cursor()
    cur.execute("DELETE FROM candidates")
    cur.executemany(sql_statement, new_record)
    conn.commit()
    return redirect('/admin/candidates')


@app.route('/admin/candidates/edit/<id>', methods=['GET','POST'])
def edit_candidates(id: int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates where id={str(id)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/candidates')
    if request.method == 'GET':
        return render_template('create-candidates.html', ph= record[1], phs=record[2], phv=record[7] , mode_name="Edit", bck_btn="../../candidates", poses=conn.execute('SELECT * from positions').fetchall())
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from candidates where id={str(id)}")
        record = cursor.fetchone()
        try:
            os.remove(f'./static/pics/{record[5]}')
        except:
            pass
        fola = request.files['photo']
        ffname = f"{''.join(random.choice('0123456789ABCDEFMJWksiwl') for i in range(6))}.{fola.filename.split('.')[-1]}"
        fola.save(f"./static/pics/{ffname}")
        name = flask.request.values.get('name') # Your form's
        std = flask.request.values.get('std')
        date = flask.request.values.get('date')
        house = flask.request.values.get('house')
        pos = flask.request.values.get('pos')
        votes = flask.request.values.get('votes')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE candidates SET name='{name}', STD='{std}', DOB='{date}', House='{house}', Photo='{ffname}', Position={pos}, Votes={votes} WHERE id = {id}")
        conn.commit()
        return redirect('/admin/candidates')


http_server = WSGIServer(('0.0.0.0', 8080), app) 
# asyncio.get_event_loop().run_in_executor(None, http_server.serve_forever)
http_server.serve_forever()
# time.sleep(50)
# http_server.stop()