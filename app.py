from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

app.route('/')
def register():
    return redirect("/register")

@app.route("/register", methods=['POST', "GET"])
def register():
    form= RegisterForm()

    if form.validate_on_submit():
        name= form.username.data
        password=form.password.data
        firstName= form.firstName.data
        lastName= form.lastName.data

        user = User.register(name, password, firstName, lastName)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.username
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)


@app.route("/login", mehtods=['POST', 'GET'])
def login():
    form = LoginForm    
    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data

        user=User.authenticate(user, password)

        if user: 
            session['user_id']= user.username
            return redirect("/secret")
        
        else: form.username.errors = ["Incorrect name/password"]
    
    return render_template("login.html", form=form)



app.route("/secret")
def secret():
    if "user_id" not in session:
        flash("you must be logged in to view")
        return redirect("/")



    else:
        return render_template('secret.html')



@app.rout('/logout')
def logout():
    session.pop('user_id')
    flash("you have been logout!")
    return redirect("/")