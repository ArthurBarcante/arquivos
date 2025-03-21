from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import database, models, schemas
from app import crud

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db,user.username)
    if db_user:
        raise
    HTTPException(status_code=400,detail="Username alreeady registered")
    return crud.create_user(db,user)