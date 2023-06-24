from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username and password match a user in the database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        )
        user = c.fetchone()

        if user is None:
            flash("Invalid login credentials", "error")
            return redirect("/")
        else:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        # Connect to the database
        conn = sqlite3.connect("database.db")
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
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            flash("Username already exists", "error")
            return redirect("/register")
        else:
            # Insert the new user into the database
            c.execute(
                "INSERT INTO users (username, password, full_name, gender, address, email, contact_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
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


if __name__ == "__main__":
    app.run(debug=True)
