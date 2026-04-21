def test_add_service(client, monkeypatch):

    monkeypatch.setattr("app.create_worker_service", lambda u, s, p: None)

    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post("/my-services", data={
        "service_id": 1,
        "price": 50
    })

    assert response.status_code == 302 or response.status_code == 200