#external imports
from flask import Flask, flash, redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

#my imports
from connect_db_test import get_db
from live_finder import *
from web_scraper import checkIfExsits


app = Flask(__name__)
app.secret_key = os.urandom(12)
db = SQLAlchemy(app)


@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/wikicheat")
    else:
        return render_template("login.html")
    

@app.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        entered_name = request.form['full_name']
        entered_email = request.form['email']
        entered_password = request.form['password']
        entered_confirm_password = request.form['confirm_password']
        entered_gender = request.form.get('gender', None)


        if not entered_name or not entered_email or not entered_password or not entered_confirm_password or not entered_gender:
            return render_template("registration.html", errormessage = "You did not enter fill out all the fields")
        if entered_password != entered_confirm_password:
            return render_template("registration.html", errormessage = "The Passwords you entered did not match")
        
        #get data from db
        cursor = get_db()
        
        #check if email already exists
        cursor.execute("SELECT email FROM users WHERE email = '{}' ".format(entered_email))
        user = cursor.fetchall()
        if len(user) > 0:
            return render_template("registration.html", errormessage = "There is already an email assigned to this account")

        hash = generate_password_hash(entered_password)
        cursor.execute("SELECT gender_id FROM gender WHERE gender='{}'".format(entered_gender))
        gender_id = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO users (full_name, email, hash, gender) VALUES ('{}', '{}', '{}', '{}');".format(entered_name, entered_email, hash, gender_id))

        return render_template("registration.html", errormessage = "The account was successfully created")


        
    else:
        if "user_id" in session:
            return redirect("/wikicheat")
        return render_template("registration.html")

 
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        #get data from form
        entered_email = request.form['email']
        entered_password = request.form['password']

        #check if data exsists
        if not entered_email or not entered_password:
            return render_template("login.html", errormessage = "You did not enter the write Data")

        #get data from db
        cursor = get_db()

        cursor.execute("SELECT user_id, email, hash FROM users WHERE email = '{}' ".format(entered_email))
        user = cursor.fetchall()

        if len(user) == 1:
            user_id = user[0][0]
            db_email = user[0][1]
            db_hash = user[0][2]
            if db_email == entered_email and check_password_hash(db_hash, entered_password):
                session['user_id'] = user_id
                return redirect("/wikicheat")
            else:
                return render_template("login.html", errormessage = "You entered the wrong login information")
        else:
            return render_template("login.html", errormessage = "Sorry, You entered the wrong email address")

    else:
        if "user_id" in session:
            return redirect("/wikicheat")
        return render_template("login.html")


@app.route("/logout")
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect("/")
 

@app.route('/wikicheat', methods=('GET', 'POST'))
def wikiCheat():
    if request.method == 'POST':
        start_link = request.form['start_link']
        end_link = request.form['end_link']

        if not start_link or not end_link:
            return render_template("wikicheat.html", errormessage = "Please enter 2 Valid Values")
        elif not checkIfExsits(start_link):
            return render_template("wikicheat.html", errormessage = "The first link you enterd does not exsits")
        elif not checkIfExsits(end_link):
            return render_template("wikicheat.html", errormessage = "The second link you enterd does not exsits")


        path_length = degree_distance(start_link, end_link)
        runtime = "22"

        user_id = session['user_id']
        cursor = get_db()
        cursor.execute("INSERT INTO wikipages (title) VALUES ('{0}') ON CONFLICT DO NOTHING;".format(start_link))
        cursor.execute("INSERT INTO wikipages (title) VALUES ('{0}') ON CONFLICT DO NOTHING;".format(end_link))
        cursor.execute("""INSERT INTO history (user_id, start_link, end_link, degrees_away) 
                        VALUES (
                            {user_id},
                            (SELECT wiki_id FROM wikiPages WHERE title='{start_link}'),
                            (SELECT wiki_id FROM wikiPages WHERE title='{end_link}'),
                            {degrees_away}
                        );""".format(user_id=user_id, start_link=start_link, end_link=end_link, degrees_away=path_length, runtime=runtime))
        cursor.close()

        return render_template("wikicheat.html", errormessage = "They are {} clicks away".format(path_length))


    else:
        if 'user_id' in session:
            return render_template("wikicheat.html")
        else:
            return redirect("/")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/settings', methods=('GET', 'POST'))
def settings():
    if request.method == 'POST':
        entered_data = {}
        entered_data['full_name'] = request.form['full_name']
        entered_data['email'] = request.form['email']
        entered_data['old_password'] = request.form['old_password']
        entered_data['new_password'] = request.form['password']
        entered_data['confirm_password'] = request.form['confirm_password']
        entered_data['gender'] = request.form.get('gender', None)
        
        cursor = get_db()
        user_id = session['user_id']
        cursor.execute("""SELECT u.full_name, u.email, u.hash, d.gender FROM users u 
                                JOIN gender d 
                                ON u.gender = d.gender_id
                                WHERE user_id = {};  
                                """.format(user_id))
        user = cursor.fetchall()
        # print(user)
        personal_data = {}
        personal_data["full_name"] = user[0][0]
        personal_data["email"] = user[0][1]
        personal_data["old_hash"] = user[0][2]
        personal_data["gender"] = user[0][3]


        if personal_data['full_name'] != entered_data['full_name']:
            cursor.execute("UPDATE users SET full_name = '{}' WHERE user_id = {};".format(entered_data['full_name'], user_id))
        if personal_data['email'] != entered_data['email']:
            cursor.execute("UPDATE users SET email = '{}' WHERE user_id = {};".format(entered_data['email'], user_id))

        if check_password_hash(personal_data['old_hash'], entered_data['old_password']):
            if not entered_data['new_password'] or not entered_data['confirm_password'] or entered_data['new_password'] != entered_data['confirm_password']:
                return render_template("settings.html", errormessage = 'There was a error with the Passwords you entered')
            else:
                new_hash = generate_password_hash(entered_data['new_password'])
                cursor.execute("UPDATE users SET hash = '{}' WHERE user_id = {};".format(new_hash, user_id))



        # print(personal_data)
        # print(entered_data)

        return render_template("settings.html", errormessage = 'Successful Query')

    
    else:
        if 'user_id' in session:

            #get data from db
            cursor = get_db()
            user_id = session['user_id']
            print(user_id)
            cursor.execute("""SELECT u.full_name, u.email, d.gender FROM users u 
                                JOIN gender d 
                                ON u.gender = d.gender_id
                                WHERE user_id = {};  
                                """.format(user_id))
            user = cursor.fetchall()
            print(user)
            personal_data = {}
            personal_data["full_name"] = user[0][0]
            personal_data["email"] = user[0][1]
            personal_data[user[0][2]] = "checked"
            print(personal_data)

            return render_template("settings.html", personal_data = personal_data)
        else:
            return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)