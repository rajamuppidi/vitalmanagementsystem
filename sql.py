import hashlib

import mysql.connector
from datetime import datetime

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Python@4650"
)

# Check if the database exists
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
databases = mycursor.fetchall()

database_exists = False
for database in databases:
    if database[0] == 'patient_info':
        database_exists = True
        break

# If the database does not exist, create it
if not database_exists:
    mycursor.execute("CREATE DATABASE patient_info")

# Connect to the new database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Python@4650",
  database="patient_info"
)
mycursor = mydb.cursor()

# Create the patient_info table
mycursor.execute("CREATE TABLE IF NOT EXISTS patient_info (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT, sex VARCHAR(10), address VARCHAR(255), contact_number VARCHAR(20), email VARCHAR(255), blood_group VARCHAR(10), weight FLOAT, height FLOAT)")

# Create the vital_signs table
mycursor.execute( "CREATE TABLE IF NOT EXISTS vital_signs (id INT AUTO_INCREMENT PRIMARY KEY, patient_id INT,  date DATE, temperature FLOAT, systolic_bp INT, diastolic_bp INT, fasting_blood_sugar FLOAT, random_blood_sugar FLOAT, postprandial_glucose FLOAT, heart_rate INT, pulse_rate INT, FOREIGN KEY (patient_id) REFERENCES patient_info(id))")

# Create the medical_conditions table
mycursor.execute("CREATE TABLE IF NOT EXISTS medical_conditions (id INT AUTO_INCREMENT PRIMARY KEY, patient_id INT, current_symptoms VARCHAR(255), FOREIGN KEY (patient_id) REFERENCES patient_info(id))")

# Create the users table
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

# Create the physician table
mycursor.execute("CREATE TABLE IF NOT EXISTS physician (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), username VARCHAR(255), password VARCHAR(255))")

# Add a default physician
username = "physician1"
password = "password123"
hashed_password = hashlib.sha256(password.encode()).hexdigest()
mycursor.execute("SELECT * FROM physician WHERE username = %s", (username,))
result = mycursor.fetchone()
if not result:
    mycursor.execute("INSERT INTO physician (name, username, password) VALUES (%s, %s, %s)", ("Physician 1", username, hashed_password))
    mydb.commit()

