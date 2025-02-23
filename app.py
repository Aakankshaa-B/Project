import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Connect to database
conn = sqlite3.connect("schemes.db")
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    income INTEGER,
                    occupation TEXT,
                    email TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS schemes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age_limit INTEGER,
                    income_limit INTEGER,
                    occupation TEXT,
                    link TEXT)''')
conn.commit()

# Custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            font-size: 50px;
            font-weight: bold;
            font-family: 'Georgia', serif;
            color: #E74C3C;
            text-align: center;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
            color: #2E86C1;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>SchemeBridge</div>", unsafe_allow_html=True)
st.markdown("<div class='title'>Government Scheme Eligibility Checker</div>", unsafe_allow_html=True)

# User Input Section
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=100)
income = st.number_input("Enter your annual income (in ₹):", min_value=0)
occupation = st.selectbox("Select your occupation:", ["Student", "Farmer", "Worker", "Self-Employed", "women"])
user_email = st.text_input("Enter your email:")

# Email sender credentials
SENDER_EMAIL = "trupthij66@gmail.com"
SENDER_PASSWORD = "zmnf icro ntva fdzj"

def send_email(recipient_email, schemes):
    subject = "Government Scheme Eligibility Result"
    body = "Congratulations! You are eligible for the following schemes:\n\n"
    body += "\n".join([f"{scheme[0]} - {scheme[1]}" for scheme in schemes]) if schemes else "Unfortunately, you are not eligible for any schemes."
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

if st.button("Check Eligibility"):
    query = "SELECT name, link FROM schemes WHERE age_limit >= ? AND income_limit >= ? AND occupation = ?"
    cursor.execute(query, (age, income, occupation))
    schemes = cursor.fetchall()

    if schemes:
        st.success("You are eligible for the following schemes:")
        for scheme in schemes:
            st.markdown(f"✅ [{scheme[0]}]({scheme[1]})")
    else:
        st.error("Sorry, you are not eligible for any schemes.")
    
    # Store user input data in the database
    cursor.execute("INSERT INTO user_data (name, age, income, occupation, email) VALUES (?, ?, ?, ?, ?)",
                   (name, age, income, occupation, user_email))
    conn.commit()
    st.success("Your details have been saved!")
    
    # Send email notification
    if user_email:
        if send_email(user_email, schemes):
            st.success("Email notification sent successfully!")

# Admin Panel for Adding New Schemes
st.sidebar.header("Admin Panel - Add New Scheme")
scheme_name = st.sidebar.text_input("Scheme Name:")
scheme_age_limit = st.sidebar.number_input("Age Limit:", min_value=0)
scheme_income_limit = st.sidebar.number_input("Income Limit (₹):", min_value=0)
scheme_occupation = st.sidebar.selectbox("Select Occupation:", ["Student", "Farmer", "Worker", "Self-Employed", "women"])
scheme_link = st.sidebar.text_input("Official Scheme Link:")

if st.sidebar.button("Add Scheme"):
    cursor.execute("INSERT INTO schemes (name, age_limit, income_limit, occupation, link) VALUES (?, ?, ?, ?, ?)",
                   (scheme_name, scheme_age_limit, scheme_income_limit, scheme_occupation, scheme_link))
    conn.commit()
    st.sidebar.success("New scheme added successfully!")

# Admin Panel for Deleting Schemes
st.sidebar.header("Admin Panel - Delete Scheme")
cursor.execute("SELECT id, name FROM schemes")
saved_schemes = cursor.fetchall()

scheme_to_delete = st.sidebar.selectbox("Select Scheme to Delete:", [f"{s[0]} - {s[1]}" for s in saved_schemes])

if st.sidebar.button("Delete Scheme"):
    scheme_id = scheme_to_delete.split(" - ")[0]
    cursor.execute("DELETE FROM schemes WHERE id = ?", (scheme_id,))
    conn.commit()
    st.sidebar.success("Scheme deleted successfully!")

# Display all stored schemes
st.sidebar.subheader("Existing Schemes")
cursor.execute("SELECT name, age_limit, income_limit, occupation, link FROM schemes")
saved_schemes = cursor.fetchall()
for scheme in saved_schemes:
    st.sidebar.markdown(f"📌 [{scheme[0]}]({scheme[4]}) (Age: {scheme[1]}, Income: ₹{scheme[2]}, Occupation: {scheme[3]})")

conn.close()

