import pytest
import sys
import os

# 🔧 Para que encuentre app y models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# 🔹 Cliente Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

# 🔹 Usuario falso
@pytest.fixture
def fake_user():
    return {
        "id": 1,
        "name": "Juan",
        "email": "juan@test.com",
        "phone": "3001234567",
        "password_hash": "fakehash",
        "role": "worker"
    }

# 🔹 Servicios falsos
@pytest.fixture
def fake_services():
    return [
        {"name": "Plomería", "price": 50},
        {"name": "Electricidad", "price": 70}
    ]