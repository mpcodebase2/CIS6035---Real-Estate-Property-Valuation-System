from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)

@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html', username=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash('You have successfully registered! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Incorrect username/password!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/list')
def list_app():
    if 'loggedin' in session:
        return render_template('list.html')
    flash('You need to be logged in to view this page.')
    return redirect(url_for('login'))

@app.route('/add_bar', methods=['POST'])
def add_bar():
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
