from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import datetime
import re

app = Flask(__name__)
app.secret_key = 'Alfie'
mysql = connectToMySQL('users')
now = datetime.datetime.now()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def renderIndex():
    return render_template("index.html")

@app.route('/process_registration',methods=['POST'])
def procRegistration():
    #Getting current emails in the database,for comparison
    current_emails = mysql.query_db("SELECT email FROM regusers")

    #first_name should be longer than 2 characters and all letters:
    if len(request.form['first_name']) < 2:
        flash("First Name must be at least 2 characters","name_error")
    elif not request.form['first_name'].isalpha():
        flash("First Name must have only letters","name_error")
    else:
        session['first_name'] = request.form['first_name']
    #last_name should be longer than 2 characters and all letters
    if len(request.form['last_name']) < 2:
        flash("Last Name must be at least 2 characters","lname_error")
    elif not request.form['last_name'].isalpha():
        flash("Last Name must be letters only","lname_error")
    else:
        session['last_name'] = request.form['last_name']
    #email address must be new and valid format
    for item in current_emails:
        if request.form['email'] == item['email']:
            flash("Email already in list!","email_error")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", "email_error")
    else:
        session['email'] = request.form['email']
    #Password must be at least 8 characters; must match confirm password
    if len(request.form['password']) < 8:
        flash("Password must have at least 8 characters","password_error")
    elif request.form['confirm_password'] != request.form['password']:
        flash("Confirm password must match original password","cpassword_error")

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        #Hashing password and adding it to session
        session['password'] = bcrypt.generate_password_hash(request.form['password'])
        session['logged_in'] = True
        data = {
                'first_name': session['first_name'],
                'last_name': session['last_name'],
                'email': session['email'],
                'password': session['password'],
                'created_at': now,
                'updated_at': now
            }
        query = "INSERT INTO regusers (first_name,last_name,email,password_hash,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(created_at)s,%(updated_at)s);"
        mysql.query_db(query, data)
        print(session)
        flash("You've been sucessfully registered!","sucess")
        return redirect('/sucess')

@app.route('/sucess')
def sucess():
    if session['logged_in'] == True:
        return render_template("logged_page.html")
    else:
        return "not allowed here"

@app.route('/login',methods=['POST'])
def logIn():
    #Getting info from the forms
    provided_email = request.form['email']
    if len(request.form['email']) < 1:
        flash("Please enter a valid email address","login_error")
    #Missing email format validation
    provided_password = request.form['password']
    if len(request.form['password']) < 1:
        flash("Please enter a valid password","login_error")

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        #Fetching current emails and passwords
        current_data = mysql.query_db("SELECT id,email,password_hash FROM regusers")

        #Checking if email is in the current data
        for item in current_data:
            if item['email'] == provided_email:
                if bcrypt.check_password_hash(item['password_hash'], provided_password):
                    session.clear()
                    session['logged_in'] = True
                    session['user_id'] = item['id']
                    session['email'] = item['email']
                    print(session)
                    return redirect('/sucess')
            
        flash("Issues with email or password","login_error")
        return redirect('/')
            

@app.route('/logout')
def sessionLogout():
    session['logged_in'] = False
    print(session)
    flash("You've been loged out!","logout")
    return redirect('/')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)