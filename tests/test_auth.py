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

# Checks if credentials are correct for an account
def test_login_correct_credentials(client):
  client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }        
  )

  response = client.post(
    "/auth/login",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }
  )

  print(response.status_code)
  print(response.json())

  assert response.status_code == 200 


# Checks if the response is valid on incorrect password 
def test_login_incorrect_password(client):
  client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }        
  )

  response = client.post(
    "/auth/login",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma0303"
    }        
  )    

  assert response.status_code == 401 


# Checks the response if someone tries to log into nonexsistent user
def test_login_nonexistent_user(client):
  response = client.post(
    "/auth/login",
    json={
      "username": "robaflex1",
      "password": "urmomma115"
    }        
  )      

  assert response.status_code == 401 


# Checks if token generation is successful after logging in 
def test_login_token_generation(client):
  client.post(
    "/auth/register",
    json={
      "username": "robaflex",
      "email": "robaflex@test.com",
      "password": "urmomma115"
    }
  )
  
  response = client.post(
    "/auth/login",
    json={
      "username": "robaflex",
      "password": "urmomma115"
    }
  )

  data = response.json() 

  assert response.status_code == 200 
  assert "access_token" in data 
  assert data["access_token"] is not None
  assert data["token_type"] == "bearer"  