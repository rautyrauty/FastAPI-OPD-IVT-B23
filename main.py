from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import time
import asyncio

import sql_app.models as models
import sql_app.schemas as schemas
from db import get_db, engine
from sql_app.repositories import TaskRepo

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


@app.post('/tasks', tags=["Task"], response_model=schemas.Task, status_code=201)
async def create_task(task_request: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create an Task and store it in the database
    """

    return await TaskRepo.create(db=db, task=task_request)


@app.get('/tasks', tags=["Task"], response_model=List[schemas.Task])
def get_all_tasks(full_name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Tasks stored in database
    """
    if full_name:
        tasks = []
        db_task = TaskRepo.fetch_by_full_name(db, full_name)
        tasks.append(db_task)
        return tasks
    else:
        return TaskRepo.fetch_all(db)


@app.get('/tasks/{task_id}', tags=["Task"], response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get the Task with the given ID provided by User stored in database
    """
    db_task = TaskRepo.fetch_by_id(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found with the given ID")
    return db_task


@app.delete('/tasks/{task_id}', tags=["Task"])
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete the Task with the given ID provided by User stored in database
    """
    db_task = TaskRepo.fetch_by_id(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found with the given ID")
    await TaskRepo.delete(db, task_id)
    return "Task deleted successfully!"


@app.put('/tasks/{task_id}', tags=["Task"], response_model=schemas.Task)
async def update_task(task_id: int, task_request: schemas.Task, db: Session = Depends(get_db)):
    """
    Update an Task stored in the database
    """
    db_task = TaskRepo.fetch_by_id(db, task_id)
    if db_task:
        update_task_encoded = jsonable_encoder(task_request)
        db_task.cert_type = update_task_encoded['cert_type']
        db_task.full_name = update_task_encoded['full_name']
        db_task.student_id = update_task_encoded['student_id']
        return await TaskRepo.update(db=db, task_data=db_task)
    else:
        raise HTTPException(status_code=400, detail="Task not found with the given ID")

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
