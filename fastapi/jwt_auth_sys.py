
# step-1 {modules}
from passlib.context import CryptContext



# step-2 {Password hashing with passlib}

# Bcrypt is a specialized password-hashing algorithm used by developers to securely store user passwords in databases.
# Never store plain passwords. I used bcrypt:
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return  pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


#step3: {JWT Encode+ Decode}

from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone

secret_key="iAtwrfNNZU7q8HtrhmWsvEQP5HYUtjYJ0wM3laHkcEP"  # In real world applications , you need to keep them in .env file to maintain the secrecy
algorithm="HS256"
access_token_expire_minutes=30

def create_access_token(data:dict, expires_delta=None):
    to_encode=data.copy()
    expire=expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))

    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,secret_key,algorithm=algorithm)

def decode_access_token(token:str):
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        return None
    

# step-4 {The Login Route}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

app=FastAPI()
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": hash_password("alice123")
    },
    "bob": {
        "username": "bob",
        "hashed_password": hash_password("bob123")
    }
    
}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# step-05 {Protecting Routes with Dependencies}


from fastapi.security import OAuth2PasswordBearer
from fastapi import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]
@app.get("/me")
def read_me(username: str = Depends(get_current_user)):
    return {"username": username}