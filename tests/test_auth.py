from werkzeug.security import generate_password_hash

def test_login_success(client, monkeypatch):

    def fake_get_user(email):
        return {
            "id": 1,
            "name": "Juan",
            "email": email,
            "password_hash": generate_password_hash("1234"),
            "role": "worker"
        }

    monkeypatch.setattr("app.get_user_by_email", fake_get_user)

    response = client.post("/login", data={
        "email": "test@test.com",
        "password": "1234"
    })

    assert response.status_code in [200, 302]


def test_login_fail(client, monkeypatch):

    def fake_get_user(email):
        return None

    monkeypatch.setattr("app.get_user_by_email", fake_get_user)

    response = client.post("/login", data={
        "email": "wrong@test.com",
        "password": "1234"
    })

    assert b"credenciales" in response.data.lower()


def test_register_success(client, monkeypatch):

    monkeypatch.setattr("app.get_user_by_email", lambda email: None)
    monkeypatch.setattr("app.create_user", lambda *args: None)

    response = client.post("/register", data={
        "name": "Juan",
        "email": "juan@test.com",
        "phone": "3001234567",
        "password": "1234",
        "confirm_password": "1234",
        "tipo_usuario": "worker"
    })

    assert response.status_code == 200
    assert b"registro exitoso" in response.data.lower()


def test_register_duplicate_email(client, monkeypatch):

    monkeypatch.setattr("app.get_user_by_email", lambda email: {"id": 1})

    response = client.post("/register", data={
        "name": "Juan",
        "email": "juan@test.com",
        "phone": "3001234567",
        "password": "1234",
        "confirm_password": "1234",
        "tipo_usuario": "worker"
    })

    assert b"registrado" in response.data.lower()