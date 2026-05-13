"""
 Project name: TPI_Kaizen_Classroom
 File : database.py
 Author : Anthony Simond
 Description: Manages database connections and executes SQL queries, including user authentication and data persistence
 Date : 2026/04/29
 Last modified : 2026/05/13
 Version : 1.2
"""
import mysql.connector
import os
from dotenv import load_dotenv
from security import check_password

load_dotenv()
def get_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def verify_login(email,password):
    """
    Verifies user credentials by checking the email in the database
    and validating the hashed password.
    :param email: the email address entered by the user
    :param password: the plaintext password to verify
    :return: A dictionary containing user data if successful, None otherwise.
    """
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    conn.close()

    if user:
        if check_password(password,user["password"]):
            return user
    return None
