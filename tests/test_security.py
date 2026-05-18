"""
 Project name: TPI_Kaizen_Classroom
 File : tests\test_security.py
 Author : Anthony Simond
 Description: Unit Test
 Date : 2026/05/12
 Last modified : 2026/05/13
 Version : 1.2
"""
from security import *

def test_hash_password_returns_string():
    """
    Check that the function returns a string (not bytes).
    :return: None
    """
    # Arrange
    password = "MonMotDePasse123"

    # Act
    result = hash_password(password)

    # Assert
    assert isinstance(result, str)
    assert result != password


def test_password_verification_success():
    """
    Verifies that a valid password matches its hash.
    :return: None
    """
    # Arrange
    raw_password = "Secret789!"
    hashed = hash_password(raw_password)

    # Act
    is_valid = check_password(raw_password, hashed)

    # Assert
    assert is_valid is True

def test_password_verification_failure():
    """
    Verifies that an invalid password does not match its hash.
    :return: None
    """
    # Arrange
    raw_password = "MonMotDePasse123"
    wrong_password = "MauvaisMDP"
    hashed = hash_password(raw_password)

    #Act
    is_valid = check_password(wrong_password, hashed)

    # Assert
    assert is_valid is False

def test_salting_produces_different_hashes():
    """
    Check that two hashes of the same password are different.
    :return: None
    """
    # Arrange
    password = "Identique123"

    # Act
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    # Assert
    assert hash1 != hash2