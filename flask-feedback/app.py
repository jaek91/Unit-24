from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()
toolbar = DebugToolbarExtension(app)

# @app.errorhandler(401)
# def unauthorized_msg_401(err):
#     return Response()

@app.route('/')
def home_page():
    return redirect("/register")

@app.route('/register', methods=["GET", "POST"])
def register_user():
    
    user_form = RegisterForm()
    ##post request for registering new user
    if user_form.validate_on_submit():
        username = user_form.username.data
        password = user_form.password.data
        first_name = user_form.first_name.data
        last_name = user_form.last_name.data
        email = user_form.email.data

        new_user = User.register(username, password, first_name, last_name, email)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash('User Created!', 'success')
        return redirect(f'/users/{new_user.username}')
    
    ##if validation fails, it's just a simple get request for the registration form
    return render_template("users/register.html", form = user_form)

@app.route("/users/<username>", methods=["GET"])
def show_secret_content(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized ##would a custom made 401 message work here?
    
    form = DeleteForm() 
    user = User.query.get(username)

    return render_template("users/details.html", user = user, form = form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if "username" not in session or username != session["username"]:
        raise Unauthorized
   
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

###---Routes involving feedback---###

@app.route("/users/<username>/feedback/add", methods=["GET","POST"])
def add_feedback(username):
    if "username" not in session or username != session["username"]:
        raise Unauthorized
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/create.html", form = form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template("feedback/edit.html", form = form, feedback = feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized

    db.session.delete(feedback)
    db.session.commit()
    
    return redirect(f"/users/{feedback.username}")



###---Routes involving login and logout---###

@app.route('/login', methods=["GET", "POST"])
def login_user():
    login_form = LoginForm()
    #post request takes care of the validation of existing user
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else: 
            login_form.username.errors = ["Invalid username or password"]
            return render_template("users/login.html", form = login_form)

    return render_template("users/login.html", form = login_form)

@app.route('/logout', methods=["GET"])
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')
