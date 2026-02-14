from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, DBTask
from task_model import TaskSchema

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(DBTask).all()


@app.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=List[TaskSchema])
def create_tasks(task: TaskSchema, db: Session = Depends(get_db)):
    new_task = DBTask(title=task.title, description=task.description, is_complete=task.is_complete)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, updated_task: TaskSchema, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.is_complete = updated_task.is_complete

    db.commit()
    db.refresh(db_task)
    return  db_task

@app.delete("task/{task_id}", response_model=TaskSchema)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    del_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if not del_task:
        raise  HTTPException(status_code=404, detail="Task not found")
    db.delete(del_task)
    db.commit()
    return del_task