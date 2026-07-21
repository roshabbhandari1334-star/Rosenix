import pytest
from backend.api.auth import hash_password, verify_password, create_access_token
from jose import jwt
from backend.config.settings import settings

def test_password_hashing():
    raw_password = "SuperSecretPassword123!"
    hashed = hash_password(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_generation():
    payload = {"sub": "user_123", "role": "ADMIN"}
    token = create_access_token(payload)
    
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "user_123"
    assert decoded["role"] == "ADMIN"
    assert "exp" in decoded