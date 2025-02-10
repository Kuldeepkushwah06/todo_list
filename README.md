# FastAPI Todo List API

A RESTful Todo List API built with FastAPI and MongoDB, featuring JWT authentication and CRUD operations.

## Features
- User Authentication with JWT
- CRUD operations for Todo items
- MongoDB database integration
- Async operations
- Secure password hashing

## Prerequisites
- Python 3.8+
- MongoDB
- Postman (for testing)

## Clone the repository
git clone https://github.com/Kuldeepkushwah06/todo_list.git
cd todo_list

## Installation & Setup

1. **Create Virtual Environment**
python -m venv venv
source venv/bin/activate # Linux/Mac

venv\Scripts\activate # Windows

2. **Install Dependencies**
pip install -r requirements.txt


3. **Configure Environment Variables**
Create `.env` file with required configurations:
- MONGODB_URL
- DATABASE_NAME
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

4. **Start MongoDB**
Windows
net start MongoDB 
Linux
sudo systemctl start mongod
Mac
brew services start mongodb-community

or use mongodb compass to start mongodb

5. **Run the Application**
uvicorn app.main:app --reload


## API Testing Guide (Postman)

### Setting Up Postman Collection
1. Open Postman
2. Click "Collections" in the sidebar
3. Click "+" to create a new collection
4. Name it "Todo API"


### 1. Register User
- **POST** `http://localhost:8000/register`
- Select "Body" tab → "raw" → "JSON"
- Example request body:
```json
{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
}
```
- Expected response (201 Created):
```json
{
    "message": "User created successfully"
}
```

### 2. Login (Get Token)
- **POST** `http://localhost:8000/token`
- Select "Body" tab → "x-www-form-urlencoded"
- Add key-value pairs:
```
username: testuser
password: password123
```
- Expected response (200 OK):
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```
- Copy the access_token value

### Setting Up Authentication
1. In Postman, click "..." next to collection name
2. Select "Edit"
3. Go to "Variables" tab
4. Add a new variable:
   - Variable: token
   - Initial Value: your_copied_token
   - Current Value: your_copied_token
5. Click "Save"

### 3. Create Todo
- **POST** `http://localhost:8000/todos/`
- Headers:
  ```
  Authorization: Bearer {{token}}
  Content-Type: application/json
  ```
- Body (raw JSON):
```json
{
    "title": "Complete Project",
    "description": "Finish the Todo API implementation",
    "completed": false
}
```
- Expected response (200 OK):
```json
{
    "id": "65fd8a...",
    "title": "Complete Project",
    "description": "Finish the Todo API implementation",
    "completed": false,
    "user_id": "65fd8...",
    "created_at": "2024-03-22T10:30:00",
    "updated_at": "2024-03-22T10:30:00"
}
```

### 4. Get All Todos
- **GET** `http://localhost:8000/todos/`
- Headers:
  ```
  Authorization: Bearer {{token}}
  ```
- No body required
- Expected response (200 OK): Array of todos

### 5. Update Todo
- **PUT** `http://localhost:8000/todos/{todo_id}`
- Replace {todo_id} with actual ID from create/get response
- Headers:
  ```
  Authorization: Bearer {{token}}
  Content-Type: application/json
  ```
- Body (raw JSON):
```json
{
    "title": "Updated Title",
    "description": "Updated description",
    "completed": true
}
```

### 6. Delete Todo
- **DELETE** `http://localhost:8000/todos/{todo_id}`
- Replace {todo_id} with actual ID
- Headers:
  ```
  Authorization: Bearer {{token}}
  ```
- No body required
- Expected response: 204 No Content

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /register | Register user | No |
| POST | /token | Login | No |
| POST | /todos/ | Create todo | Yes |
| GET | /todos/ | List todos | Yes |
| PUT | /todos/{id} | Update todo | Yes |
| DELETE | /todos/{id} | Delete todo | Yes |

## Common Issues & Solutions

1. **MongoDB Connection Error**
   - Verify MongoDB is running
   - Check connection string in .env

2. **Authentication Error**
   - Ensure correct username/password
   - Verify token format
   - Check token expiration

3. **Request Error**
   - Verify request body format
   - Check required fields
   - Ensure proper Content-Type header
