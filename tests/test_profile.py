def test_profile_requires_login(client):

    response = client.get("/profile")

    assert response.status_code == 302  # redirect


def test_profile_worker(client, monkeypatch, fake_user, fake_services):

    monkeypatch.setattr("app.get_user_by_id", lambda id: fake_user)
    monkeypatch.setattr("app.get_services_by_worker", lambda id: fake_services)

    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["role"] = "worker"

    response = client.get("/profile")

    assert response.status_code == 200
    assert b"Plomer" in response.data
    assert b"50" in response.data


def test_profile_client(client, monkeypatch, fake_user):

    fake_user["role"] = "client"

    monkeypatch.setattr("app.get_user_by_id", lambda id: fake_user)

    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["role"] = "client"

    response = client.get("/profile")

    assert response.status_code == 200