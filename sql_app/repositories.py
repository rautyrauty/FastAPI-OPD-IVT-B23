
from sqlalchemy.orm import Session

from . import models, schemas


class TaskRepo:
    
 async def create(db: Session, task: schemas.TaskCreate):
        db_task = models.Task(cert_type=task.cert_type, student_id=task.student_id, full_name=task.full_name)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
 def fetch_by_id(db: Session,_id):
     return db.query(models.Task).filter(models.Task.id == _id).first()
 
 def fetch_by_full_name(db: Session,name):
     return db.query(models.Task).filter(models.Task.full_name == full_name).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Task).offset(skip).limit(limit).all()
 
 async def delete(db: Session,task_id):
     db_task= db.query(models.Task).filter_by(id=task_id).first()
     db.delete(db_task)
     db.commit()
     
     
 async def update(db: Session,task_data):
    updated_task = db.merge(task_data)
    db.commit()
    return updated_task
