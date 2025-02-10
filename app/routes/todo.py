from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models import Todo, TodoCreate, User
from ..database import todo_collection
from ..auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Todo)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new todo item.
    """
    todo_dict = todo.dict()
    todo_dict["user_id"] = str(current_user["_id"])
    todo_dict["created_at"] = datetime.utcnow()
    todo_dict["updated_at"] = datetime.utcnow()
    
    result = await todo_collection.insert_one(todo_dict)
    created_todo = await todo_collection.find_one({"_id": result.inserted_id})
    return created_todo

@router.get("/", response_model=List[Todo])
async def read_todos(current_user: User = Depends(get_current_user)):
    """
    Retrieve all todos for the current user.
    """
    todos = await todo_collection.find({"user_id": str(current_user["_id"])}).to_list(1000)
    return todos

@router.get("/{todo_id}", response_model=Todo)
async def read_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific todo by ID.
    """
    if (todo := await todo_collection.find_one({"_id": ObjectId(todo_id), "user_id": str(current_user["_id"])})):
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: str,
    todo: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a todo item.
    """
    todo_dict = todo.dict()
    todo_dict["updated_at"] = datetime.utcnow()
    
    if (await todo_collection.find_one({"_id": ObjectId(todo_id), "user_id": str(current_user["_id"])})):
        update_result = await todo_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": todo_dict}
        )
        if update_result.modified_count == 1:
            if (updated_todo := await todo_collection.find_one({"_id": ObjectId(todo_id)})):
                return updated_todo
    
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a todo item.
    """
    delete_result = await todo_collection.delete_one({"_id": ObjectId(todo_id), "user_id": str(current_user["_id"])})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found") 