from flask import Flask, g, request, render_template
import sqlite3

app = Flask(__name__, template_folder='templates')

# render the base template
@app.route("/")
def base():
    return render_template('base.html')

# function to access the database
def get_message_db(): 
    try:    # return database if exists
          return g.message_db   
    except:
        # create data base if it doesn't exist
          g.message_db = sqlite3.connect("message.db")
          cursor = g.message_db.cursor()
          query = """
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER IDENTITY PRIMARY KEY,
            name TEXT,
            message TEXT
            );
            """
          cursor.execute(query)
          g.message_db.commit() 
          return g.message_db

# function to update database with new submissions
def insert_message(request):
    conn = get_message_db()               # connect to database
    cursor = conn.cursor()

    messages = request.form["message"]    # extract messages
    names = request.form["name"]          # extract names

    query = """
       INSERT INTO messages (name, message)
       VALUES ('{}','{}');
        """.format(names, messages)
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
                                    messages = request.form["message"])
        except:
            return render_template('submit.html', error=True)

# function to view messages
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
    return entries

# render view template
@app.route("/view/")
def view():
    entries = random_messages(3)
    return render_template('view.html', entries = entries)