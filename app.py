from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm

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
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form= RegisterForm()

    if form.validate_on_submit():
        name= form.username.data
        password=form.password.data
        firstName= form.firstName.data
        lastName= form.lastName.data

        user = User.register(name, password, firstName, lastName)
        db.session.add(user)
        db.session.commit()

        session["username"] = User.username
        return redirect(f'/users/{user.username}')
    else:
        return render_template('users/register.html', form=form)


@app.route("/login", mehtods=['POST', 'GET'])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm
    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data

        user=User.authenticate(user, password)

        if user:
            session['username']= User.username
            return redirect(f"/users/{user.username}")

        else:
             form.username.errors = ["Incorrect name/password"]
             return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.rout('/logout')
def logout():
    session.pop('username')
    flash("you have been logout!")
    return redirect("/")



@app.route('/users/<username>')
def show_user(username):
    if "username" not in session:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)

@app.route("/users/<username/delete>", methods=["POST"])
def remove_user(username):
    if "username" not in session:
        raise unauthorized()

    user=User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def add_new_feedback(username):
    if username not in session:
        raise Unauthorized()
    form = FeedbackForm
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template ("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET","POST"])
def  update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session["username"]:
        raise unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title
        feedback.content = form.content
        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    return render_template('/feedback/edit.html', form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session["username"]:
        raise unauthorized()
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f'/users/{feedback.username}')







