from models import get_user_by_id, get_services_by_worker
from unittest.mock import patch

def test_get_user_by_id(fake_user):

    with patch("models.get_connection") as mock_conn:

        mock_cursor = mock_conn.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = fake_user

        user = get_user_by_id(1)

        assert user["name"] == "Juan"
        assert user["email"] == "juan@test.com"


def test_get_services(fake_services):

    with patch("models.get_connection") as mock_conn:

        mock_cursor = mock_conn.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = fake_services

        servicios = get_services_by_worker(1)

        assert len(servicios) == 2
        assert servicios[0]["name"] == "Plomería"