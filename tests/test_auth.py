from core.security import verify_password
from models.models import User


# ----------- REGISTER ------------

# Checks if the registration of an account was successful
def test_successful_registration(client):
  response = client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }
  )
  
  assert response.status_code == 200

# Checks if the provided email is already used by another account
def test_duplicate_email(client): 
  client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }    
  )

  response = client.post(
    "/auth/register",
    json={
      "username": "robaflex77",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }    
  )

  assert response.status_code == 409

# Checks if provided data is valid 
def test_invalid_data(client):
  response = client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex-email-com",
      "password": "urmomma115"
    }
  )

  assert response.status_code == 422 

# Checks if password hashing feature worked on accounts password
def test_hashed_password(client, db):
  response = client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }    
  )

  assert response.status_code == 200

  user = db.query(User).filter(User.email == "robaflex@test.com").first()

  assert user is not None 
  assert user.hashed_password != "urmomma115"
  assert verify_password("urmomma115", user.hashed_password)


# ----------- LOGIN ------------
