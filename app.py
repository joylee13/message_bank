from flask import Flask, g, request, render_template
import sqlite3

app = Flask(__name__)

# render the base template

@app.route("/")
def base():
    return render_template('base.html')

def get_message_db(): 
    # sql command to create if it doesn't exist yet
    query = """
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER,
            name TEXT,
            message TEXT
            );
            """
    try:    # return database if exists
          return g.message_db   
    except: # create data base if it doesn't exist
          g.message_db = sqlite3.connect("message_db.sqlite")
          cursor = g.message_db.cursor()
          cursor.execute(query)

          g.message_db.commit() 
          return g.message_db


def insert_message(request):
    conn = get_message_db()               # connect to database
    cursor = conn.cursor()

    messages = request.form["message"]    # extract messages
    names = request.form["name"]          # extract names
    ids = len(g.message_db.index) + 1     # create id numbers

    query = """
       INSERT INTO messages (id, name, message)
       VALUES ('{},'{}','{}');
        """.format(ids, names, messages)
    cursor.execute(query)

    conn.commit()   # save message
    conn.close()    # close connection


# render the submit template
@app.route("/submit/", methods = ["GET", "POST"])
def submit():
    if request.method == 'GET':
            return render_template('submit.html')
    else:
        try:
            insert_message(request)
            return render_template('submit.html', 
                                    names = request.form["name"],
                                    messages = request.form["message"],
                                    thanks = True)
        except:
            return render_template('submit.html', error=True)

def random_messages(n):
    query = """
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {};
    """.format(n)

    conn = get_message_db()
    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    entries = [(row[1], row[2]) for row in rows]

    conn.close()
    return [entries]

@app.route("/view/", methods = ["GET"])
def view():
    entries = random_messages(1)
    return render_template('view.html', entries = entries)