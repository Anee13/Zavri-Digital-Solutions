from flask import Flask, render_template, request
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)

# ---------------- EMAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aneeshkannan0013@gmail.com'
app.config['MAIL_PASSWORD'] = 'sukn vuwb ogjw kluo'

mail = Mail(app)

# ---------------- MYSQL CONFIG ----------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "zavri_database"

# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    # Step 1: Connect to MySQL server
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Step 2: Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.database = DB_NAME

    # Step 3: Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            mobile VARCHAR(50),
            service VARCHAR(100),
            subject VARCHAR(200),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Initialize DB on startup
init_db()

# ---------------- ROUTES ----------------
@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/services.html")
def services_page():
    return render_template("services.html")

@app.route("/career.html")
def career_page():
    return render_template("career.html")

@app.route("/contact.html")
def contact_page():
    return render_template("contact.html")

@app.route("/academic_portal.html")
def academic_portal():
    return render_template("academic_portal.html")


# ---------------- CONTACT FORM SUBMIT ----------------
@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    data = request.form

    # Combine country code + mobile
    mobile = f"{data['country_code']} {data['mobile']}"

    # Connect to DB
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Insert data
    cursor.execute("""
        INSERT INTO contact (name, email, mobile, service, subject, message)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["name"],
        data["email"],
        mobile,
        data["service"],
        data["subject"],
        data["message"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    # Send Email
    msg = Message(
        subject=f"New Contact Form: {data['subject']}",
        sender=app.config['MAIL_USERNAME'],
        recipients=["aneeshkannan0013@gmail.com"]
    )
    msg.body = f"""
Name: {data['name']}
Email: {data['email']}
Mobile: {mobile}
Service: {data['service']}

Message:
{data['message']}
"""
    mail.send(msg)

    return "success"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)


