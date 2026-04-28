"""
 Project name: TPI_Kaizen_Classroom
 File : security.py
 Author : Anthony Simond
 description: Consilidates the application's security features, including password hashing and verification using the Bcrypt library
 Date : 2026/04/28
 last modified : 2026/04/28
 Version : 1.0
"""
import bcrypt

def hash_password(password : str) -> str:
    """
    Takes a plaintext password,hashes it,and returns the hash.
    Returns the hash as a string.(UTF-8)

    :param password: the plaintext password entered by the user
    :return: The secure hash, ready to be stored in the database
    """

    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode('utf-8')


def check_password(password : str, hashed_password : str) -> bool:
    """
    Compares a plaintext password with a stored hash.
    Returns true if they match, False otherwise.
    :param password: the plaintext password to be verified (login attempt)
    :param hashed_password: the hash retrieved from the database
    :return: True if the password matches the hash, False otherwise
    """

    password_bytes = password.encode('utf-8')
    hashed_bytes =  hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)
