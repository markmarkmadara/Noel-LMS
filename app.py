from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    jsonify,
    send_file,
)
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key = "your-secret-key"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Flask-Mail configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "bcplms.qc@gmail.com"
app.config["MAIL_PASSWORD"] = "gpyxnpypngilmhef"
app.config["MAIL_DEFAULT_SENDER"] = "bcplms.qc@gmail.com"

# Initialize Flask-Mail
mail = Mail(app)


# Route for adding an event
@app.route("/events", methods=["POST"])
def add_event():
    title = request.form["title"]
    start = request.form["start"]
    end = request.form["end"]

    # Insert the event into the database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO events (title, start, end)
        VALUES (?, ?, ?)
    """,
        (title, start, end),
    )
    conn.commit()
    conn.close()

    return jsonify(message="Event added successfully")


# Route for deleting an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Delete the event from the database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

    return jsonify(message="Event deleted successfully")


# Route for fetching events
@app.route("/events")
def get_events():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, start, end FROM events")
    events = [
        {"id": row[0], "title": row[1], "start": row[2], "end": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()

    return jsonify(events)


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


@app.route("/admin_courses", methods=["GET", "POST"])
def admin_dashboard_courses():
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
        # Form to add a course
        if request.method == "POST":
            week_title = request.form.get("week_title")
            content_title = request.form.get("content_title")
            course = request.form.get("course")
            uploaded_files = request.files.getlist("pdf")
            file = request.files["pdf"]
            for file in uploaded_files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    unique_filename = str(uuid.uuid4()) + "-" + filename
                    file.save(
                        os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
                    )
                    save_to_database(week_title, content_title, unique_filename, course)
        # Pass the user details to the template for rendering
        return render_template(
            "admin_courses.html",
            user=user,
            weeks_cpe222=get_weeks("CPE 222"),
            get_contents_cpe222=get_contents,
            weeks_cpe221=get_weeks("CPE 221"),
            get_contents_cpe221=get_contents,
        )
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
        return render_template(
            "courses.html",
            user=user,
            weeks_cpe222=get_weeks("CPE 222"),
            get_contents_cpe222=get_contents,
            weeks_cpe221=get_weeks("CPE 221"),
            get_contents_cpe221=get_contents,
        )
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

    # Retrieve both non-admin and admin users from the database
    c.execute("SELECT * FROM users")
    all_users = c.fetchall()

    # Close the database connection
    conn.close()

    return render_template("admin_students.html", user=user, users=all_users)


@app.route("/edit_user_role", methods=["POST"])
def edit_user_role():
    user_id = request.form.get("user_id")
    new_role = request.form.get("new_role")

    # Connect to the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Update the user role in the database
    c.execute("UPDATE users SET is_admin=? WHERE id=?", (new_role, user_id))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    flash("User role updated successfully", "success")
    return redirect("/admin_students")


# Admin Delete User
@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")

    # Connect to the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Delete the user from the database
    c.execute("DELETE FROM users WHERE id=?", (user_id,))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    flash("User deleted successfully", "success")
    return redirect("/admin_students")


# Admin Register
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
        role = int(request.form["role"])

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
                    role,
                ),
            )
            conn.commit()
            conn.close()
            flash("Registration successful. You can now log in.", "success")
            # Send the email with credentials
            send_credentials_email(email, username, password)
            return redirect("/")

    return render_template("register.html", is_admin=is_admin)


# Create a function to send email with credentials
def send_credentials_email(email, username, password):
    subject = "Login Credentials"
    body = f"Username: {username}\nPassword: {password}"
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)


@app.route("/testread", methods=["GET"])
def view_weeks_pdf():
    return render_template(
        "testread.html",
        weeks_cpe222=get_weeks("CPE 222"),
        get_contents_cpe222=get_contents,
        weeks_cpe221=get_weeks("CPE 221"),
        get_contents_cpe221=get_contents,
    )


@app.route("/view_pdf/<int:pdf_id>", methods=["GET"])
def view_pdf(pdf_id):
    with app.app_context():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT filename, content_title FROM pdfs WHERE id = ?", (pdf_id,)
        )
        result = cursor.fetchone()
        if result:
            filename, content_title = result
            return send_file(
                os.path.join(app.config["UPLOAD_FOLDER"], filename),
                mimetype="application/pdf",
            )
    return "File not found"


@app.route("/testcourses", methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        week_title = request.form.get("week_title")
        content_title = request.form.get("content_title")
        course = request.form.get("course")
        uploaded_files = request.files.getlist("pdf")
        file = request.files["pdf"]
        for file in uploaded_files:
            if file.filename:
                filename = secure_filename(file.filename)
                unique_filename = str(uuid.uuid4()) + "-" + filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_filename))
                save_to_database(week_title, content_title, unique_filename, course)
    return render_template(
        "testcourses.html",
        weeks_cpe222=get_weeks("CPE 222"),
        get_contents_cpe222=get_contents,
        weeks_cpe221=get_weeks("CPE 221"),
        get_contents_cpe221=get_contents,
    )


def save_to_database(week_title, content_title, filename, course):
    with app.app_context():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pdfs (week_title, content_title, filename, course) VALUES (?, ?, ?, ?)",  # noqa: E501
            (week_title, content_title, filename, course),
        )
        conn.commit()


def get_weeks(course):
    with app.app_context():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT week_title FROM pdfs WHERE course = ?", (course,)
        )
        weeks = cursor.fetchall()
        return weeks


def get_contents(week_title, course):
    with app.app_context():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT content_title, id FROM pdfs WHERE week_title = ? AND course = ?",
            (week_title, course),
        )
        contents = cursor.fetchall()
    return contents


@app.route("/read_pdf/<int:pdf_id>", methods=["GET"])
def read_pdf(pdf_id):
    with app.app_context():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM pdfs WHERE id = ?", (pdf_id,))
        result = cursor.fetchone()
        if result:
            filename = result[0]
            return send_file(
                os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=False
            )
    return "File not found"


@app.route("/delete_pdf/<int:pdf_id>", methods=["POST"])
def delete_pdf(pdf_id):
    with app.app_context():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM pdfs WHERE id = ?", (pdf_id,))
        result = cursor.fetchone()
        if result:
            filename = result[0]
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            cursor.execute("DELETE FROM pdfs WHERE id = ?", (pdf_id,))
            conn.commit()

    # Retrieve the user details from the database
    user_id = session["user_id"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return render_template(
        "admin_courses.html",
        user=user,
        weeks_cpe222=get_weeks("CPE 222"),
        get_contents_cpe222=get_contents,
        weeks_cpe221=get_weeks("CPE 221"),
        get_contents_cpe221=get_contents,
    )


if __name__ == "__main__":
    app.run(debug=True)
