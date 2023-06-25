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

            # Check if the user is an admin
            if user[8] == 1:
                # User is an admin
                return redirect("/admin_dashboard")
            else:
                # User is not an admin, redirect to regular dashboard
                return redirect("/index")

    return render_template("login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
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

        # Check if the user exists and is an admin
        if user is None or not user[8]:  # Assuming `is_admin` is at index 8
            flash("Access denied", "error")
            return redirect("/")

        # Pass the user details to the template for rendering
        return render_template("admin_dashboard.html", user=user)
    else:
        return redirect("/")


@app.route("/admin_profile")
def admin_dashboard_profile():
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

        # Check if the user exists and is an admin
        if user is None or not user[8]:  # Assuming `is_admin` is at index 8
            flash("Access denied", "error")
            return redirect("/")

        # Pass the user details to the template for rendering
        return render_template("admin_profile.html", user=user)
    else:
        return redirect("/")


@app.route("/index")
def index():
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
        return render_template("index.html", user=user)
    else:
        return redirect("/")


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


@app.route("/courses")
def courses():
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
        return render_template("courses.html", user=user)
    else:
        return redirect("/")


@app.route("/update", methods=["GET", "POST"])
def update_user():
    if "user_id" in session:
        if request.method == "POST":
            # Retrieve the form data
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            full_name = request.form.get("full_name")
            contact_number = request.form.get("contact_number")
            email = request.form.get("email")
            address = request.form.get("address")

            # Basic form validation
            if (
                not username
                or not password
                or not confirm_password
                or not full_name
                or not contact_number
                or not email
                or not address
            ):
                flash("Please fill in all the fields", "error")
                return redirect("/update")

            if password != confirm_password:
                flash("Password and confirm password do not match", "error")
                return redirect("/update")

            # Connect to the database and update the user information
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            # Get the user ID from the session
            user_id = session["user_id"]

            # Update the user information in the database
            c.execute(
                "UPDATE users SET username=?, password=?, full_name=?, contact_number=?, email=?, address=? WHERE id=?",  # noqa: E501
                (
                    username,
                    password,
                    full_name,
                    contact_number,
                    email,
                    address,
                    user_id,
                ),
            )

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()

            flash("User information updated successfully", "success")
            return redirect("/dashboard")
        else:
            # Retrieve the user details and render the edit form
            # Connect to the database
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            # Get the user ID from the session
            user_id = session["user_id"]

            # Retrieve the user details from the database
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            user = c.fetchone()

            # Check if the user exists
            if user is None:
                flash("User not found", "error")
                return redirect("/")

            # Close the database connection
            conn.close()

            # Pass the user details to the template for rendering
            return render_template("edit.html", user=user)
    else:
        return redirect("/")


@app.route("/update_admin", methods=["GET", "POST"])
def update_admin():
    if "user_id" in session:
        if request.method == "POST":
            # Retrieve the form data
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            full_name = request.form.get("full_name")
            contact_number = request.form.get("contact_number")
            email = request.form.get("email")
            address = request.form.get("address")

            # Basic form validation
            if (
                not username
                or not password
                or not confirm_password
                or not full_name
                or not contact_number
                or not email
                or not address
            ):
                flash("Please fill in all the fields", "error")
                return redirect("/update")

            if password != confirm_password:
                flash("Password and confirm password do not match", "error")
                return redirect("/update")

            # Connect to the database and update the user information
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            # Get the user ID from the session
            user_id = session["user_id"]

            # Update the user information in the database
            c.execute(
                "UPDATE users SET username=?, password=?, full_name=?, contact_number=?, email=?, address=? WHERE id=?",  # noqa: E501
                (
                    username,
                    password,
                    full_name,
                    contact_number,
                    email,
                    address,
                    user_id,
                ),
            )

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()

            flash("User information updated successfully", "success")
            return redirect("/admin_profile")
        else:
            # Retrieve the user details and render the edit form
            # Connect to the database
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            # Get the user ID from the session
            user_id = session["user_id"]

            # Retrieve the user details from the database
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            user = c.fetchone()

            # Check if the user exists
            if user is None:
                flash("User not found", "error")
                return redirect("/")

            # Close the database connection
            conn.close()

            # Pass the user details to the template for rendering
            return render_template("admin_edit.html", user=user)
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/admin_students")
def admin_students():
    if "user_id" in session:
        # Connect to the database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # Get the user ID from the session
        user_id = session["user_id"]

        # Retrieve the user details from the database
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = c.fetchone()

        # Check if the user exists
        if user is None:
            flash("User not found", "error")
            return redirect("/")
    else:
        user = None

    # Connect to the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Retrieve the non-admin users from the database
    c.execute("SELECT * FROM users WHERE is_admin=0")
    non_admin_users = c.fetchall()

    # Close the database connection
    conn.close()

    return render_template("admin_students.html", user=user, users=non_admin_users)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        user_id = session["user_id"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
        user = c.fetchone()
        conn.close()

        if user and user[0] == 1:
            # User is logged in as an admin
            is_admin = True
        else:
            # User is not logged in as an admin
            is_admin = False
    else:
        is_admin = False

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        address = request.form["address"]
        confirm_password = request.form["confirm_password"]
        email = request.form["email"]
        contact_number = request.form["contact_number"]
        gender = request.form["gender"]
        is_admin = request.form["is_admin"]

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
                "INSERT INTO users (username, password, full_name, gender, address, email, contact_number, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",  # noqa: E501
                (
                    username,
                    password,
                    full_name,
                    gender,
                    address,
                    email,
                    contact_number,
                    is_admin,
                ),
            )
            conn.commit()
            conn.close()
            flash("Registration successful. You can now log in.", "success")
            return redirect("/")

    return render_template("register.html", is_admin=is_admin)


@app.route("/fec_week1")
def week1():
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
        return render_template("Electronics/fec_week1.html", user=user)
    else:
        return redirect("/")


@app.route("/fec_week2")
def fec_week2():
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
        return render_template("Electronics/fec_week2.html", user=user)
    else:
        return redirect("/")


@app.route("/sd_week1")
def sd_week1():
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
        return render_template("Software/sd_week1.html", user=user)
    else:
        return redirect("/")


@app.route("/sd_week2")
def sd_week2():
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
        return render_template("Software/sd_week2.html", user=user)
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
