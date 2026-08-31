def test_authenticated_user_can_create_task(client):
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

  token = login_response.json()["access_token"]

  response = client.post(
    "/tasks",
    headers={
      "Authorization": f"Bearer {token}"
    },
    json={
      "title": "Write Pytest tests",
      "description": "Write tests for my Task API",
      "priority": 5,
      "due_date": None
    }
  )

  assert response.status_code == 201
  assert response.json()["title"] == "Write Pytest tests"
  assert response.json()["priority"] == 5


def test_unauthenticated_user_can_create_task(client):
  response = client.post(
    "/tasks",
    json={
      "title": "Write Pytest tests",
      "description": "Write tests for my Task API",
      "priority": 5,
      "due_date": None
    }
  )

  assert response.status_code == 401


def invalid_task_data(client):
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
  
  token = login_response.json()["access_token"]

  response = client.post(
    "/tasks",
    headers={
      "Authorization": f"Bearer {token}"
    },
    json={
      "title": "Message A.K",
      "description": "Try to get a dialogue going",
      "priority": "5",
      "due_date": 2009
    }
  )

  assert response.status_code == 422