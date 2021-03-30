from fastapi import FastAPI, status, Depends, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from . import schemas, models
from .schemas import Todo


app = FastAPI()

models.Base.metadata.create_all(engine)

templates = Jinja2Templates(directory="./Todo/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/')
# def get_all(db: Session = Depends(get_db)):
#     all_todo = db.query(models.Todo).all()
#     return all_todo

@app.get('/', response_class=HTMLResponse)
def get_all(request: Request, db: Session = Depends(get_db)):
    all_todo = db.query(models.Todo).all()
    return templates.TemplateResponse('todo.html', {'request': request, 'All_todos': all_todo})


@app.post('/todo', status_code=status.HTTP_201_CREATED)
def create(name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new = models.Todo(name=name, description=description)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get('/todo/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
def get_one(todo_id: int, request: Request, db: Session = Depends(get_db)):
    a_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if a_todo:
        return templates.TemplateResponse("todo.html", {'request': request, 'a_todo': a_todo})
    else:
        raise HTTPException(status_code=404, detail=f"No Item With {todo_id}")


# @app.get('/todo/{todo_id}', response_class=HTMLResponse, response_model=Todo)
# def get_one(request: Request, todo_id: int):
#     return templates.TemplateResponse("todo.html", {'request': request, 'ID': todo_id})


@app.delete('/todo/{todo_id}')
def delete(todo_id: int, db: Session = Depends(get_db)):
    del_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    if not del_todo:
        return {'Detail': 'Item Want To Delete Not Found'}
    else:
        db.commit()
        return {'Details': f'The Item With {todo_id} has Deleted'}


@app.put('/todo/{todo_id}')
def update(todo_id: int, request: schemas.Todo, db: Session = Depends(get_db)):
    todo_update = db.query(models.Todo).filter(models.Todo.id == todo_id)
    if not todo_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The Todo With {todo_id} Not Found')
    else:
        todo_update.update(
            {'name': request.name, 'description': request.description}
        )
        db.commit()
        return request
