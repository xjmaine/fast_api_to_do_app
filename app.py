'''
Start the app: py -m  uvicorn app:app --reload
or
py -m fastapi dev app.py
'''

from fastapi import FastAPI, Depends, Request, Form, status, HTTPException
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from databases.database import engine, get_db_connection
from models.models import Base
from models import models

main = FastAPI()

print('creating database tables...')
Base.metadata.create_all(bind=engine)
print('Database tables created')

templates = Jinja2Templates(directory="templates")


    
# @main.get("/")
# async def read_root():
#     return {"message": "App is running and table creation is handled on startup."}


@main.get("/")
async def home(req: Request, db: Session = Depends(get_db_connection)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("base.html", {"request": req, "todo_list": todos})

@main.post("/todos")
def add_todo(req: Request, title: str = Form(...), db: Session = Depends(get_db_connection)):
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_todo = models.Todo(title=title.strip())
    db.add(new_todo)
    db.commit()
    url = main.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@main.get("/update/{todo_id}")
def update_todo(req: Request, todo_id: int, db: Session = Depends(get_db_connection)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.complete = not todo.complete
    db.commit()
    url = main.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@main.get("/delete/{todo_id}")
def delete_todo(req: Request, todo_id: int, db: Session = Depends(get_db_connection)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    url = main.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
