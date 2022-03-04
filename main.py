from flask_compress import Compress
from flask_socketio import SocketIO
from flask_session import Session
import flask, sqlite3, socket, asyncio, random, os, re, pandas as pd, tempfile, base64, re, json
from flask import abort, redirect, request, session, url_for
from flask import Flask, render_template


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

with open('config.json', 'r') as cfg:
    CFG = json.loads(cfg.read())


try:
    print(get_ip_address())
except OSError:
    print("No Network Found, Pls connect To A Network To Work For Other Devices, At This Time You cant access This App In Other Devices")
app = Flask(__name__)
socketio = SocketIO(app,)
compress = Compress()
compress.init_app(app)
conn = sqlite3.connect('data/voting.db', check_same_thread=False)
conn.execute("""CREATE TABLE IF NOT EXISTS positions (
	            id INTEGER PRIMARY KEY,
	            name TEXT NOT NULL,
	            wcs TEXT NOT NULL
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS candidates (
	            id INTEGER PRIMARY KEY,
	            name TEXT NOT NULL,
	            STD TEXT NOT NULL,
                House TEXT NOT NULL,
                Photo TEXT NOT NULL,
                Position INTEGER NOT NULL,
                Votes INTEGER NOT NULL
                );""")
conn.execute("""CREATE TABLE IF NOT EXISTS voters (
                adnumber INTEGER NOT NULL,
                name TEXT NOT NULL,
                STD TEXT NOT NULL,
                House TEXT NOT NULL,
                Voted INTEGER NOT NULL
                );""")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

@app.route('/admin')
def index():
    if not session.get("login"):
        return redirect("/admin/login")
    return render_template('index.html')

@app.route('/admin/positions')
def positions():
    if not session.get("login"):
        return redirect("/admin/login")
    return render_template('positions.html', tm=conn.cursor().execute('SELECT * from positions').fetchall())

@app.route('/admin/positions/create', methods=['GET', 'POST'])
def create():
    if not session.get("login"):
        return redirect("/admin/login")
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
    if not session.get("login"):
        return redirect("/admin/login")
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
    sql_statement_c = 'INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?)'
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
    if not session.get("login"):
        return redirect("/admin/login")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates")
    record = cursor.fetchall()
    print(record)
    cursor.execute(f"SELECT * FROM positions")
    recordpos = cursor.fetchall()
    new_r = []
    for i in recordpos:
        for u,j in enumerate(record):
            print(j, u)
            if i[0] == j[5]:
                j = list(j)
                j[5] = i[1]
                # print(tuple(j), u)
                new_r.append(tuple(j))
                # record.pop(u)
    print(new_r)
    return render_template('candidates.html', tm=new_r)

@app.route('/admin/candidates/create', methods=['GET', 'POST'])
def createc():
    if not session.get("login"):
        return redirect("/admin/login")
    if request.method == 'GET':
        return render_template('create-candidates.html', ph="", phs=0, mode_name="Create", bck_btn="../candidates", poses=conn.execute('SELECT * from positions').fetchall())
    if request.method == 'POST':
        fola = request.files['photo']
        ffname = f"{''.join(random.choice('0123456789ABCDEFMJWksiwl') for i in range(6))}.{fola.filename.split('.')[-1]}"
        fola.save(f"./static/pics/{ffname}")
        name = flask.request.values.get('name') # Your form's
        std = flask.request.values.get('std')
        house = flask.request.values.get('house')
        pos = flask.request.values.get('pos')
        votes = flask.request.values.get('votes')
        conn.execute(f"INSERT INTO candidates (name, STD, House, Photo, Position, Votes) VALUES ('{name}', '{std}', '{house}', '{ffname}', {pos}, {votes})")
        conn.commit()   
        return redirect('/admin/candidates')


@app.route('/admin/candidates/delete/<id>')
def delete_candidate(id):
    if not session.get("login"):
        return redirect("/admin/login")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates where id={str(id)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/candidates')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates where id != {str(id)}")
    record2 = cursor.fetchall()
    os.remove(f'./static/pics/{record[4]}')
    new_record = []
    for o in record2:
        pl = list(o)
        pl[0] = None
        al = tuple(pl)
        new_record.append(al)
    sql_statement = 'INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?)'
    cur = conn.cursor()
    cur.execute("DELETE FROM candidates")
    cur.executemany(sql_statement, new_record)
    conn.commit()
    return redirect('/admin/candidates')


@app.route('/admin/candidates/edit/<id>', methods=['GET','POST'])
def edit_candidates(id: int):
    if not session.get("login"):
        return redirect("/admin/login")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from candidates where id={str(id)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/candidates')
    if request.method == 'GET':
        return render_template('create-candidates.html', ph= record[1], phs=record[2], phv=record[6] , mode_name="Edit", bck_btn="../../candidates", poses=conn.execute('SELECT * from positions').fetchall())
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from candidates where id={str(id)}")
        record = cursor.fetchone()
        try:
            os.remove(f'./static/pics/{record[4]}')
        except:
            pass
        fola = request.files['photo']
        ffname = f"{''.join(random.choice('0123456789ABCDEFMJWksiwl') for i in range(6))}.{fola.filename.split('.')[-1]}"
        fola.save(f"./static/pics/{ffname}")
        name = flask.request.values.get('name') # Your form's
        std = flask.request.values.get('std')
        house = flask.request.values.get('house')
        pos = flask.request.values.get('pos')
        votes = flask.request.values.get('votes')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE candidates SET name='{name}', STD='{std}', House='{house}', Photo='{ffname}', Position={pos}, Votes={votes} WHERE id = {id}")
        conn.commit()
        return redirect('/admin/candidates')

@app.route('/admin/voters')
def voters():
    if not session.get("login"):
        return redirect("/admin/login")
    return render_template('voters.html', rec=conn.cursor().execute('SELECT * from voters').fetchall())

class devnull:
    write = lambda _: None

@app.route('/admin/voters/create', methods=['GET', 'POST'])
def vcreate():
    if not session.get("login"):
        return redirect("/admin/login")
    if request.method == 'GET':
        return render_template('create-voters-manual.html')
    if request.method == 'POST':
        ad_num = request.values.get('ad')
        name = request.values.get('name')
        std = request.values.get('std')
        house = request.values.get('house')
        voted = request.values.get('voted')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO voters (adnumber, name, STD, House, Voted) VALUES ({str(ad_num)}, '{name}', '{std}', '{house}', {str(voted)})")
        conn.commit()
        return redirect('/admin/voters')

@app.route('/admin/voters/delete/<ad>')
def delv(ad ):
    if not session.get("login"):
        return redirect("/admin/login")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from voters where adnumber={str(ad)}")
    record = cursor.fetchone()
    if record is None:
        return redirect('/admin/voters')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from voters where adnumber != {str(ad)}")
    record2 = cursor.fetchall()
    cursor.execute("DELETE FROM voters")
    cursor.executemany("INSERT INTO voters VALUES (?,?,?,?,?)", record2)
    conn.commit()
    return redirect('/admin/voters')


@app.route('/admin/voters/excel')
def vexcel():
    if not session.get("login"):
        return redirect("/admin/login")
    return render_template('create-voters-excel.html')

@app.route('/upload/vexcel', methods=['POST'])
def uexcel():
    file = request.files['file'].read()
    try:
        tf = tempfile.NamedTemporaryFile(suffix='.xlsx')
        tf.write(file)
            # print(tf.name)
        df = pd.read_excel(tf.name, engine='openpyxl')
        df['Voted'] = 0
        df.to_sql('voters', con=conn, if_exists='append', index=False)
        tf.close()
        socketio.emit('sleep', {'done': 'ok'})
        return "Ok"
    except:
        tf.close()
        socketio.emit('sleeep', {'done': 'ok'})
        return abort(500)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        passwd = request.form.get('password')
        if CFG['admin']['USERNAME'] == name and CFG['admin']['PASSWORD'] == passwd:
            session["login"] = "Yea"
            return redirect('/admin')
        else:
            return render_template('login.html', error="Error: Login Credentials Are Wrong!")
    return render_template('login.html')

@app.route('/admin/cleardata/positions')
def cdpos():
    if not session.get("login"):
        return redirect("/admin/login")
    conn.cursor().execute("DELETE from positions;").execute("DELETE from candidates")
    dir = './static/pics'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    conn.commit()
    return redirect('/admin')

@app.route('/admin/cleardata/candidates')
def cdcad():
    if not session.get("login"):
        return redirect("/admin/login")
    conn.cursor().execute("DELETE from candidates")
    dir = './static/pics'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    conn.commit()
    return redirect('/admin')

@app.route('/admin/cleardata/voters')
def cdvot():
    if not session.get("login"):
        return redirect("/admin/login")
    conn.cursor().execute("DELETE from voters")
    conn.commit()
    return redirect('/admin')


@app.route('/admin/cleardata/all')
def cdall():
    if not session.get("login"):
        return redirect("/admin/login")
    conn.cursor().execute("DELETE from voters;").execute(" Delete from candidates;").execute("delete from positions")
    dir = './static/pics'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    conn.commit()
    return redirect('/admin')

socketio.run(app, host=CFG['HOST'], port=CFG['PORT'])
# http_server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketServer) 
# asyncio.get_event_loop().run_in_executor(None, http_server.serve_forever)
# http_server.serve_forever()
# time.sleep(50)
# http_server.stop()