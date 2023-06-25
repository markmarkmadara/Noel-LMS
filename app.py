import sqlite3
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from flask_vite import Vite


class FlaskVue(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(
        dict(
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="[[",
            variable_end_string="]]",
            comment_start_string="<#",
            comment_end_string="#>",
        )
    )


app = FlaskVue(__name__, static_folder="static")
app.config["VITE_DEV_MODE"] = app.config.get("DEBUG")
app.secret_key = "your-secret-key"

Vite(app)


@app.route("/src/assets/<path:path>")
def serve_vite_assets(path):
    if app.config.get("DEBUG"):
        return send_from_directory("./src/assets/", path)
    else:
        return ("Missing resource", 404)


@app.route("/")
def index():
    return render_template("index.html")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username and password match a user in the database
        conn = sqlite3.connect("./database/database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        )
        user = c.fetchone()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")
        else:
            flash("Invalid username or password")
            return redirect("/login")

    return render_template("login.html", form=form)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        address = request.form["address"]
        confirm_password = request.form["confirm_password"]
        email = request.form["email"]
        contact_number = request.form["contact_number"]
        gender = request.form["gender"]

        # Check if the password and confirm password fields match
        if password != confirm_password:
            flash("Password and Confirm Password do not match", "error")
            return redirect("/register")

        # Check if the username already exists in the database
        conn = sqlite3.connect("./database/database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            flash("Username already exists", "error")
            return redirect("/register")
        else:
            # Insert the new user into the database
            c.execute(
                "INSERT INTO users (username, password, full_name, gender, address, email, contact_number) VALUES (?, ?, ?, ?, ?, ?, ?)",  # noqa: E501
                (
                    username,
                    password,
                    full_name,
                    gender,
                    address,
                    email,
                    contact_number,
                ),
            )
            conn.commit()
            flash("Registration successful. You can now log in.", "success")
            return redirect("/")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        # Connect to the database
        conn = sqlite3.connect("./database/database.db")
        c = conn.cursor()

        # Get the user ID from the session
        user_id = session["user_id"]

        # Retrieve the user details from the database
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = c.fetchone()

        # Close the database connection
        conn.close()

        # Check if the user exists
        if user is None:
            flash("User not found", "error")
            return redirect("/")

        # Pass the user details to the template for rendering
        return render_template("dashboard.html", user=user)
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )
