from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .routes import todo
from .models import UserCreate, Token
from .auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from .database import user_collection

app = FastAPI(title="Todo API", description="A simple Todo API with authentication")

# Include todo routes
app.include_router(todo.router, prefix="/todos", tags=["todos"])

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Register a new user.
    """
    if await user_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    await user_collection.insert_one(user_dict)
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get access token for authentication.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to Todo API"} 