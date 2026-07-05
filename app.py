from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "yams_secret_key_2026"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "yams123":
            session['logged_in'] = True
            return redirect('/admin')

        return "Invalid Username or Password"

    return render_template('login.html')


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/login')

    search = request.args.get("search", "")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if search:
        cursor.execute("""SELECT * 
                   FROM applications
                   WHERE archived = 0
                   AND(
                   fullname LIKE ?
                   OR phone LIKE ?
                   OR service LIKE ?
                   )
                   ORDER BY id DESC
                   """, (f"%{search}%", f"%{search}%", f"{search}%"))
    else:
        cursor.execute("""SELECT * 
                       FROM applications
                       WHERE archived = 0
                       ORDER BY id DESC
                  """)

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        applications=applications
    )


@app.route('/archived')
def archived():
    if not session.get('logged_in'):
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * 
                   FROM applications
                   WHERE archived = 1
                   ORDER BY completed_date DESC
                   """)
    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "archived.html",
        applications=applications
    )


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')


@app.route("/start/<int:id>")
def start(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE applications
    SET status='In progress'
    WHERE id=?
    """, (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status='Completed',
         completed_date=?
    WHERE id=?
    """, (datetime.now().strftime("%Y-%m-%d"), id))
    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/archive/<int:id>")
def archive(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET archived=1,
       completed_date = COALESCE(completed_date, ?)
    WHERE id = ?
    """, (datetime.now().strftime("%Y-%m-%d"), id))

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/restore/<int:id>")
def restore(id):
    if not session.get('logged_in'):
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET archived = 0
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/archived")


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        service = request.form['service']
        description = request.form['description']
        service_date = request.form['date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO applications
        (fullname, phone, email, location,
         service, description, service_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
                       (fullname, phone, email,
                        location, service,
                        description, service_date))

        conn.commit()
        conn.close()

        return "<h2>Application Submitted Successfully!</h2>"

    return render_template('apply.html')


if __name__ == '__main__':
    app.run(debug=True)
