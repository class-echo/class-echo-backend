from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import class_schema
from app.crud import class_crud

router = APIRouter(prefix="/classes", tags=["Classes"])

@router.post("/", response_model=class_schema.ClassOut)
def create(class_: class_schema.ClassCreate, db: Session = Depends(get_db)):
    return class_crud.create_class(db, class_)

@router.get("/", response_model=list[class_schema.ClassOut])
def read_classes(db: Session = Depends(get_db)):
    return class_crud.get_classes(db)

@router.get("/{class_id}", response_model=class_schema.ClassOut)
def read_class(class_id: int, db: Session = Depends(get_db)):
    class_ = class_crud.get_class(db, class_id)
    if class_ is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    class_ = class_crud.delete_class(db, class_id)
    if class_ is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted"}
