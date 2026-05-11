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