from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DATABASE="dict.db"

app=Flask(__name__)
bcrypt=Bcrypt(app)
app.secret_key="ryokun7926"

# Getting data from database
def create_connection(db_file):
    try:
        connection=sqlite3.connect(db_file)
        return connection
    except Error as err:
        print(err)
    return None

def execute(db_file, query):
    con=create_connection(db_file)
    cur=con.cursor()
    executed=cur.execute(query)
    con.commit()
    con.close()
    return executed

def fetch(db_file, query):
    con=create_connection(db_file)
    cur=con.cursor()
    cur.execute(query)
    fetched=cur.fetchone()
    con.commit()
    con.close()
    return fetched

def search(db_file, query, input):
    con=create_connection(db_file)
    cur=con.cursor()
    print(input)
    cur.execute(query, (input,))
    list=cur.execute()
    con.close()
    return list

# Logging status
def is_logged_in():
    if session.get('email') is None:
        return False
    else:
        return True

def logged():
    log="Not logged in"
    if is_logged_in():
        log=f"Logged in as {session.get('user_category')} ({session.get('user_fname')} {session.get('user_lname')})"
    return log


# App routes
@app.route('/')
def render_homepage():
    return render_template('home.html', logged_in=is_logged_in(), log=logged())


# Account
@app.route('/signup', methods=['POST', 'GET'])
def render_signup():
    if is_logged_in():
        return redirect("/")
    if request.method == "POST":
        user_fname=request.form.get('user_fname').title().strip()
        user_lname=request.form.get('user_lname').title().strip()
        email=request.form.get('email').lower().strip()
        password=request.form.get('password')
        password2=request.form.get('password2')
        user_category=request.form.get('category')
        if password != password2:
            return redirect("/signup?error=Passwords+do+not+match")
        if len(password) < 8:
            return redirect("/signup?error=Password+must+be+at+least+8+characters")
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        id_count=int(fetch(DATABASE, f'SELECT COUNT (*) FROM users')[0]) + 1
        fetch(DATABASE, f'INSERT INTO users (user_id, user_fname, user_lname, user_email, user_pass, user_category) VALUES ({id_count}, "{user_fname}", "{user_lname}", "{email}", "{hashed_password}", "{user_category}")')
        session['email']=email
        session['id']=id_count
        session['user_fname']=user_fname
        session['user_lname']=user_lname
        session['user_category']=user_category
        return redirect("/")
    return render_template('signup.html', logged_in=is_logged_in(), log=logged())


@app.route('/login', methods=['POST', 'GET'])
def render_login():
    if is_logged_in():
        return redirect("/")
    if request.method == "POST":
        email=request.form['email'].strip().lower()
        password=request.form['password'].strip()
        try:
            user_id=fetch(DATABASE, f'SELECT user_id FROM users WHERE user_email="{email}"')[0]
            user_fname=fetch(DATABASE, f'SELECT user_fname FROM users WHERE user_email="{email}"')[0]
            user_lname=fetch(DATABASE, f'SELECT user_lname FROM users WHERE user_email="{email}"')[0]
            db_password=fetch(DATABASE, f'SELECT user_pass FROM users WHERE user_email="{email}"')[0]
            user_category=fetch(DATABASE, f'SELECT user_category FROM users WHERE user_email="{email}"')[0]
        except IndexError:
            return redirect("/login?error=Invalid+username+or+password")
        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+valid+or+password+incorrect")
        session['email']=email
        session['id']=user_id
        session['user_fname']=user_fname
        session['user_lname']=user_lname
        session['user_category']=user_category
        return redirect("/")
    return render_template('login.html', logged_in=is_logged_in(), log=logged())


@app.route('/logout')
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect('/?message=See+you+next+time!')


# Deletion
@app.route('/delete')
def render_delete_category():
    if not is_logged_in():
        return redirect("/")
    else:
        naming=session['user_fname'] + " " + session['user_lname']
        return render_template("delete.html", type="account", name=naming, logged_in=is_logged_in(), log=logged())


@app.route('/delete_account')
def delete_account():
    execute(DATABASE, f"DELETE FROM users WHERE user_id={session.get('id')}")
    [session.pop(key) for key in list(session.keys())]
    return redirect('/?message=Account+is+successfully+deleted!')

