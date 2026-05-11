from enum import verify

import pytest
from security import *

def test_hash_password_returns_string():
    """
    Check that the function returns a string (not bytes).
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
    """
    # Arrange
    raw_password = "Secret789!"
    hashed = hash_password(raw_password)

    # Act
    is_valid = check_password(raw_password, hashed)

    # Assert
    assert is_valid is True
