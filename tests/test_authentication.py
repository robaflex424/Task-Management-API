from datetime import datetime, timedelta, timezone
from jose import jwt 
from core.config import JWT_ALGORITHM, JWT_EXPIRATION, JWT_SECRET_KEY

# Checks if returned jwt is valid for get requests on tasks
def test_valid_jwt(client):
  client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }
  )

  login_response = client.post(
    "/auth/login",
    json={
      "username": "robaflex",
      "password": "urmomma115"
    }
  )

  assert login_response.status_code == 200

  token = login_response.json()["access_token"]

  response = client.get(
    "/tasks",
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 200


# Checks if response is valid on invalid JWT
def test_invalid_jwt(client):
  response = client.get(
    "/tasks",
    headers={"Authorization": f"Bearer some-fake-token"}
  )

  assert response.status_code == 401


# Checks if response is valid on expired JWT
def test_expired_jwt(client):
  expired_token = jwt.encode(
    {
      "sub": "1",
      "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
    },
    JWT_SECRET_KEY,
    algorithm=JWT_ALGORITHM
  )

  response = client.get(
    "/tasks",
    headers={
      "Authorization": f"Bearer {expired_token}"
    }
  )

  assert response.status_code == 401


# Checks if response is valid on GET request when JWT isnt provided
def test_missing_token(client):
  response = client.get("/tasks")

  assert response.status_code == 401