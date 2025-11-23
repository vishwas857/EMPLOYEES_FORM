from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# -------- DATABASE CONNECTION ---------
def get_connection():
    return mysql.connector.connect(
        host="localhost",    # or your MySQL host
        user="root",         # your MySQL username
        password="8571",     # your MySQL password
        database="mydatabase" # database must exist
    )

# -------- INITIALIZE DATABASE --------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            gender VARCHAR(20) NOT NULL,
            location VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

init_db()


# -------- ROUTES ---------

# Form page
@app.route('/', methods=['GET', 'POST'])
def form():
    form_data = {"name": "", "gender": "", "location": "", "phone": ""}
    if request.method == 'POST':
        # Get form data
        form_data["name"] = request.form.get('name')
        form_data["gender"] = request.form.get('gender')
        form_data["location"] = request.form.get('location')
        form_data["phone"] = request.form.get('phone')

        # Save to MySQL
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employee_details (name, gender, location, phone) VALUES (%s, %s, %s, %s)",
            (form_data["name"], form_data["gender"], form_data["location"], form_data["phone"])
        )
        conn.commit()
        cursor.close()
        conn.close()

    return render_template('form.html', data=form_data)


# Employees table page
@app.route('/employees')
def show_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_details")
    employees = cursor.fetchall()  # list of tuples
    cursor.close()
    conn.close()
    return render_template('employees.html', employees=employees)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
