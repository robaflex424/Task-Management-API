# -----------   TASK   CREATION   TESTS   -----------

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


def test_invalid_task_data(client):
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
      "priority": "hello",
      "due_date": 2009
    }
  )

  assert response.status_code == 422


# -----------   TASK   RETRIEVAL   TESTS   -----------
def test_get_all_users_tasks(client):
  
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

  client.post(
    "/tasks",
    headers={
      "Authorization": f"Bearer {token}"
    },
    json={
      "title": "message A.K",
      "description": "get a dialogue going",
      "priority": 5,
      "due_date": None
    }
  )
  response = client.get(
    "/tasks",
    headers={
      "Authorization": f"Bearer {token}"
    }
  )

  assert response.status_code == 200
  assert len(response.json()) == 1
  assert response.json()[0]["title"] == "message A.K"

def test_get_individual_task(client):
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
  
  # Token
  token = login_response.json()["access_token"]

  create_response = client.post(
    "/tasks",
    headers={
      "Authorization": f"Bearer {token}"
    },
    json={
      "title": "message A.K",
      "description": "get a dialogue going",
      "priority": 5,
      "due_date": None
    }
  )

  # Task id
  task_id = create_response.json()["id"]

  response = client.get(
    f"/tasks/{task_id}",
    headers={
      "Authorization": f"Bearer {token}"
    }
  )

  assert response.status_code == 200
  assert response.json()["id"] == task_id
  assert response.json()["title"] == "message A.K"
  assert response.json()["priority"] == 5

def test_get_nonexistent_task(client):
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

  response = client.get(
    f"/tasks/5",
    headers={
      "Authorization": f"Bearer {token}"
    }
  )  

  assert response.status_code == 404

def test_user_cant_access_another_user_task(client):
# Creating user robaflex
  client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }
  )

  login_response_robaflex = client.post(
    "/auth/login",
    json={
      "username": "robaflex",
      "password": "urmomma115"
    }
  )
  
  token_robaflex = login_response_robaflex.json()["access_token"]

  create_task = client.post(
    "/tasks",
    headers={
      "Authorization":f"Bearer {token_robaflex}"
    },
    json={
      "title": "message A.K",
      "description": "some description A.K",
      "priority": 5,
      "due_date": None
    }
  )

  task_id = create_task.json()["id"]

  # Create user AK

  client.post(
    "/auth/register",
    json={
      "username": "user_AK",
      "email": "ak@test.com",
      "password": "urmomma0303"
    }
  )
  
  login_response_ak = client.post(
    "/auth/login",
    json={
      "username": "user_AK",
      "password": "urmomma0303"
    }
  )

  token_ak = login_response_ak.json()["access_token"]

  response = client.get(
    f"/tasks/{task_id}",
    headers={
      "Authorization": f"Bearer {token_ak}"
    }
  )

  assert response.status_code == 404