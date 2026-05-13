"""
 Project name: TPI_Kaizen_Classroom
 File : seed_users.py
 Author : Anthony Simond
 Description: Script to populate the database with initial administrative and teacher accounts using secure password hashing.
 Date : 2026/04/29
 Last modified : 2026/05/13
 Version : 1.2
"""

import mysql.connector
from security import hash_password
import  os
from dotenv import load_dotenv

load_dotenv()
def seed():
    """
    Populates the 'users' table with initial data.
    Hashes passwords using Bcrypt before insertion to ensure database security.

    :return: None
    """
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    cursor = conn.cursor()

    users = [
        ("Simond","Anthony", "anthony.simond@eduvaud.ch", hash_password("admin123"), "Admin"),
        ("Favre", "Raphael", "raphael.favre@eduvaud.ch", hash_password("fr123"), "Enseignant")
    ]

    query = "INSERT INTO users (lastname, firstname, email, password, role) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.executemany(query, users)
        conn.commit()
        print(f"Succès :  {cursor.rowcount} utilisateurs crées avec hash Bcrypt ! ")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
