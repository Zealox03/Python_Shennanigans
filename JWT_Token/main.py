# Import Libraries
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Define Secret Key
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to Create Access Token
def create_access_token(data: dict):
    to_encode = data.copy()
    print(f"Data to Encode: {to_encode}")
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(f"Token Expiration Time: {expire}")

    to_encode.update({"exp": expire})
    print(f"Data with exp: {to_encode}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print (f"Encoded JWT: {encoded_jwt}")

    return encoded_jwt

# Creating a Login Endpoint
app = FastAPI()

fake_user = {
    "username": "admin",
    "password": "admin_123"
}

# Verify and decode the token before permitting access to protected route
def verify_token(access_token: str):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")
        username = payload.get("username")

        return username

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

# Protected route
@app.get("/protected")
def protected_route(access_token: str):
    user = verify_token(access_token)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": f"Welcome {user}, you have access to the protected route!"}

@app.post("/login")
def login(username: str, password: str):
    # Comment: Username and password must be validated in the /login route
    if username != fake_user["username"] or password != fake_user["password"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"username": username})
    return {"access_token": access_token, "token_type": "bearer"}


# Function call for created access token
if __name__ == "__main__":
    created_token = create_access_token({"username": "user123"})
    print(f"Generated JWT Token: {created_token}")

    decoded_username = verify_token(created_token)
    print(f"Decoded Username from Token: {decoded_username}")







