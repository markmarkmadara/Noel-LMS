from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

# Database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS administrators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                gender TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                address TEXT NOT NULL
            )''')

conn.commit()

# Decorator for admin access control
def admin_required(route_function):
    def decorator_function(*args, **kwargs):
        if 'role' in session and session['role'] == 'admin':
            return route_function(*args, **kwargs)
        else:
            # Redirect to student dashboard or show an error message
            return redirect('/student/dashboard')
    
    # Preserve the original function name and attributes
    decorator_function.__name__ = route_function.__name__
    decorator_function.__doc__ = route_function.__doc__
    
    return decorator_function

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin/register', methods=['GET', 'POST'])
@admin_required
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Add any additional fields you want to capture during admin registration

        # Insert admin information into the database
        c.execute("INSERT INTO administrators (username, password, email) VALUES (?, ?, ?)",
                  (username, password, email))
        conn.commit()

        return redirect('/admin/dashboard')

    return render_template('admin_registration.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Fetch admin data from the database
    c.execute("SELECT * FROM administrators")
    administrators = c.fetchall()

    return render_template('admin_dashboard.html', administrators=administrators)

@app.route('/student/registration', methods=['GET', 'POST'])
def student_registration():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']

        # Insert student information into the database
        c.execute("INSERT INTO students (first_name, middle_name, last_name, email, username, password, "
                  "date_of_birth, gender, phone_number, address) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (first_name, middle_name, last_name, email, username, password, date_of_birth,
                   gender, phone_number, address))
        conn.commit()

        return redirect('/student/dashboard')

    return render_template('student_registration.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    return render_template('student_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    # Fetch student data from the database
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    return render_template('student_dashboard.html', students=students)

@app.route('/student/profile/<int:student_id>')
def student_profile(student_id):
    # Fetch student data from the database based on the student_id
    c.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = c.fetchone()

    return render_template('student_profile.html', student=student)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
