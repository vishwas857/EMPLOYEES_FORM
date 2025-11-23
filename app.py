from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load local .env if exists (for local testing)
load_dotenv()
#this is the change that i have made to the code

# Database config from environment
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# Validate environment variables
missing_vars = [v for v in ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"] if not os.getenv(v)]
if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

# Connect to MySQL
def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

# Initialize database
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

# Routes
@app.route('/', methods=['GET', 'POST'])
def form():
    form_data = {"name": "", "gender": "", "location": "", "phone": ""}
    if request.method == 'POST':
        form_data["name"] = request.form.get('name')
        form_data["gender"] = request.form.get('gender')
        form_data["location"] = request.form.get('location')
        form_data["phone"] = request.form.get('phone')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employee_details (name, gender, location, phone) VALUES (%s, %s, %s, %s)",
            (form_data["name"], form_data["gender"], form_data["location"], form_data["phone"])
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/employees')

    return render_template('form.html', data=form_data)

@app.route('/employees')
def show_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_details")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('employees.html', employees=employees)

# Railway uses PORT environment variable
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0")
