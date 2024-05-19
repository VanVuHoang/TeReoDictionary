from flask import Flask, render_template, request, redirect, session
import sqlite3, os
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DATABASE="dict.db"

app=Flask(__name__)
bcrypt=Bcrypt(app)
app.secret_key="vuhoang"


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
    cur.execute(query)
    fetched=cur.fetchall()
    con.commit()
    con.close()
    return fetched

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
        log=f"Logged in as {session.get('user_category')} ({session.get('user_username')})"
    return log

def status(category):
    if session.get('user_category') == category:
        return True
    
def credentials(email):
    db_password=fetch(DATABASE, f'SELECT user_pass FROM users WHERE user_email="{email}"')[0]
    user_id=fetch(DATABASE, f'SELECT user_id FROM users WHERE user_email="{email}"')[0]
    user_fname=fetch(DATABASE, f'SELECT user_fname FROM users WHERE user_email="{email}"')[0]
    user_lname=fetch(DATABASE, f'SELECT user_lname FROM users WHERE user_email="{email}"')[0]
    user_username=fetch(DATABASE, f'SELECT user_username FROM users WHERE user_email="{email}"')[0]
    user_category=fetch(DATABASE, f'SELECT user_category FROM users WHERE user_email="{email}"')[0]
    return [db_password, user_id, user_fname, user_lname, user_username, user_category]


# Word
## Display word
@app.route('/')
def render_all():
    word_tuple=execute(DATABASE, f'SELECT word_name, word_translation, type_name, word_definition, user_id, image_name, record_id FROM words INNER JOIN types ON words.word_type=types.type_id INNER JOIN records ON words.word_id=records.word_id INNER JOIN images ON words.word_image=images.image_id')
    user_dict = {}
    user_tuple=execute(DATABASE, f'SELECT user_id, user_username FROM users')
    for user in user_tuple:
        user_dict[user[0]] = user[1]
    type_tuple=execute(DATABASE, f'SELECT type_id, type_name FROM types')
    return render_template('home.html', words=word_tuple, types=type_tuple, users=user_dict, logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))

@app.route('/type=<word_type>')
def render_word(word_type):
    if word_type != "favicon.ico":
        type_id=fetch(DATABASE, f'SELECT type_id FROM types WHERE LOWER(type_name)="{word_type}"')[0]
        word_tuple=execute(DATABASE, f'SELECT word_name, word_translation, type_name, word_definition, user_id, image_name, record_id FROM words INNER JOIN types ON words.word_type=types.type_id INNER JOIN records ON words.word_id=records.word_id INNER JOIN images ON words.word_image=images.image_id WHERE words.word_type={type_id}')
        user_dict = {}
        user_tuple=execute(DATABASE, f'SELECT user_id, user_username FROM users')
        for user in user_tuple:
            user_dict[user[0]] = user[1]
        type_tuple=execute(DATABASE, f'SELECT type_id, type_name FROM types')
        return render_template('home.html', words=word_tuple, types=type_tuple, users=user_dict, logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))
    return ""


## Search word
@app.route('/search') 
def search(): 
    query = request.args.get('query') 
    word_tuple=execute(DATABASE, f'SELECT word_name, word_translation, type_name, word_definition, user_id, image_name, record_id FROM words INNER JOIN types ON words.word_type=types.type_id INNER JOIN records ON words.word_id=records.word_id INNER JOIN images ON words.word_image=images.image_id WHERE LOWER(word_name)=LOWER("{query}") OR LOWER(word_translation)=LOWER("{query}")')
    user_dict = {}
    user_tuple=execute(DATABASE, f'SELECT user_id, user_username FROM users')
    for user in user_tuple:
        user_dict[user[0]] = user[1]
    type_tuple=execute(DATABASE, f'SELECT type_id, type_name FROM types')
    return render_template('home.html', words=word_tuple, types=type_tuple, users=user_dict, logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))


# Account
## Signup & Login
@app.route('/signup_account', methods=['POST', 'GET'])
def render_signup():
    if is_logged_in():
        return redirect("/")
    if request.method == "POST":
        user_fname=request.form.get('user_fname').title().strip()
        user_lname=request.form.get('user_lname').title().strip()
        user_username=request.form.get('user_username').strip()
        email=request.form.get('email').lower().strip()
        password=request.form.get('password')
        password2=request.form.get('password2')
        user_category=request.form.get('category')
        if password != password2:
            return redirect("/signup_account?error=Passwords+do+not+match")
        if len(password) < 8:
            return redirect("/signup_account?error=Password+must+be+at+least+8+characters")
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        id_count=int(fetch(DATABASE, f'SELECT COUNT (*) FROM users')[0]) + 1
        execute(DATABASE, f'INSERT INTO users (user_id, user_fname, user_lname, user_username, user_email, user_pass, user_category) VALUES ({id_count}, "{user_fname}", "{user_lname}", "{user_username}", "{email}", "{hashed_password}", "{user_category}")')
        session['email']=email
        session['password']=password
        session['id']=id_count
        session['user_fname']=user_fname
        session['user_lname']=user_lname
        session['user_username']=user_username
        session['user_category']=user_category
        return redirect("/?message=Signup+successful!")
    return render_template('account/signup.html', logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))

@app.route('/login_account', methods=['POST', 'GET'])
def render_login():
    if is_logged_in():
        return redirect("/")
    if request.method == "POST":
        email=request.form['email'].lower().strip()
        password=request.form['password'].strip()
        try:
            credentials(email)
        except TypeError:
            return redirect("/login_account?error=Invalid+username+or+password")
        if not bcrypt.check_password_hash(credentials(email)[0], password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")
        session['email']=email
        session['password']=credentials(email)[0]
        session['id']=credentials(email)[1]
        session['user_fname']=credentials(email)[2]
        session['user_lname']=credentials(email)[3]
        session['user_username']=credentials(email)[4]
        session['user_category']=credentials(email)[5]
        return redirect("/?message=Login+successful!")
    return render_template('account/login.html', logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))


## Logout & Delete account
@app.route('/logout_account')
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect('/?message=Logout+successful!')

@app.route('/delete_account')
def delete_account():
    execute(DATABASE, f"DELETE FROM users WHERE user_id={session['id']}")
    [session.pop(key) for key in list(session.keys())]
    return redirect('/?message=Account+is+successfully+deleted!')


## Edit account
@app.route('/edit_account', methods=['POST', 'GET'])
def render_edit():
    if not is_logged_in():
        return redirect("/")
    if request.method == "POST":
        if request.form.get('user_fname') != None:
            user_fname=request.form.get('user_fname').title().strip()
        else:
            user_fname=session['user_fname']

        if request.form.get('user_lname') != None:
            user_lname=request.form.get('user_lname').title().strip()
        else:
            user_lname=session['user_lname']

        if request.form.get('user_username') != None:
            user_username=request.form.get('user_username').strip()
        else:
            user_username=session['user_username']

        if request.form.get('email') != None:
            email=request.form.get('email').lower().strip()
        else:
            email=session['email']

        if request.form.get('password') != None:
            password=request.form.get('password')
        else:
            password=session['password']

        if request.form.get('password2') != None:
            password2=request.form.get('password2')
        else:
            password2=session['password']

        if request.form.get('category') != None:
            user_category=request.form.get('category')
        else:
            user_category=session['user_category']

        if password != password2:
            return redirect("/edit_account?error=Passwords+do+not+match")
        if len(password) < 8:
            return redirect("/edit_account?error=Password+must+be+at+least+8+characters")
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        id = credentials(session.get('email'))[1]
        execute(DATABASE, f'UPDATE users SET user_email = "{email}" WHERE user_id = {id}')
        execute(DATABASE, f'UPDATE users SET user_pass = "{hashed_password}" WHERE user_id = {id}')
        execute(DATABASE, f'UPDATE users SET user_fname = "{user_fname}" WHERE user_id = {id}')
        execute(DATABASE, f'UPDATE users SET user_lname = "{user_lname}" WHERE user_id = {id}')
        execute(DATABASE, f'UPDATE users SET user_username = "{user_username}" WHERE user_id = {id}')
        execute(DATABASE, f'UPDATE users SET user_category = "{user_category}" WHERE user_id = {id}')
        session['email']=email
        session['user_fname']=user_fname
        session['user_lname']=user_lname
        session['user_username']=user_username
        session['user_category']=user_category
        return redirect("/?message=Account+is+successfully+edited!")
    return render_template('account/edit.html', logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))


# Admin
## Add word
@app.route('/add_word')
def render_addword():
    if not is_logged_in():
        return redirect('/?message=Need+to+be+logged+in.')
    type_tuple=execute(DATABASE, f'SELECT type_id, type_name FROM types')
    word_tuple=execute(DATABASE, f'SELECT word_id, word_name FROM words')
    image_tuple=execute(DATABASE, f'SELECT image_id, image_name FROM images WHERE image_id != 1')
    return render_template("admin/add_word.html", logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"), types=type_tuple, words=word_tuple, images=image_tuple)

@app.route('/adding_word', methods=['POST'])
def add_word():
    if not is_logged_in():
        return redirect('/?message=Need+to+be+logged+in.')
    if request.method == "POST":
        word_name=request.form.get('word_name').title().strip()
        word_translation=request.form.get('word_translation').title().strip()
        word_type=request.form.get('word_type').split(", ")[0]
        word_definition=request.form.get('word_definition').title().strip()
        if request.form.get('word_image') != None:
            word_image=request.form.get('word_image').split(", ")[0]
        else:
            word_image=1
        word_id_count=int(fetch(DATABASE, f'SELECT COUNT (*) FROM words')[0]) + 1
        execute(DATABASE, f'INSERT INTO words (word_id, word_name, word_translation, word_type, word_definition, word_image) VALUES ({word_id_count}, "{word_name}", "{word_translation}", "{word_type}", "{word_definition}", "{word_image}")')
        record_id_count=int(fetch(DATABASE, f'SELECT COUNT (*) FROM records')[0]) + 1
        execute(DATABASE, f'INSERT INTO records (record_id, word_id, user_id) VALUES ({record_id_count}, {word_id_count}, {session["id"]})')
        return redirect("/?message=Word+is+successfully+added!")
    return render_template("admin/add_word.html", logged_in=is_logged_in(), log=logged(), teacher=status("Teacher"))


## Delete word
@app.route('/deleting_word/<record_id>')
def deleting_word(record_id):
    if not is_logged_in():
        return redirect('/?message=Need+to+be+logged+in.')
    word_id=fetch(DATABASE, f'SELECT words.word_id FROM words INNER JOIN records ON words.word_id=records.word_id WHERE record_id={record_id}')[0]
    execute(DATABASE, f'DELETE FROM words WHERE word_id={word_id}')
    execute(DATABASE, f'DELETE FROM records WHERE record_id={record_id}')
    index=int(fetch(DATABASE, f'SELECT COUNT (*) FROM words')[0]) + 1 - word_id
    for i in range(0, index):
        execute(DATABASE, f'UPDATE words SET word_id = "{word_id + i}" WHERE word_id = {word_id + i + 1}')
        execute(DATABASE, f'UPDATE records SET record_id = "{word_id + i}" WHERE word_id = {word_id + i + 1}')
        execute(DATABASE, f'UPDATE records SET word_id = "{word_id + i}" WHERE word_id = {word_id + i + 1}')
    return redirect("/?message=Word+is+successfully+deleted!")