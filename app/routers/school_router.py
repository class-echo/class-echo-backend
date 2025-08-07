from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.school_schema import SchoolOut, SchoolCreate
from app.crud import school_crud as school_crud

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.post("/", response_model=SchoolOut)
def create(school: SchoolCreate, db: Session = Depends(get_db)):
    return school_crud.create_school(db, school)

@router.get("/{school_id}", response_model=SchoolOut)
def read(school_id: int, db: Session = Depends(get_db)):
    db_school = school_crud.get_school(db, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school

@router.get("/", response_model=list[SchoolOut])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return school_crud.get_all_schools(db, skip=skip, limit=limit)

@router.delete("/{school_id}", response_model=SchoolOut)
def delete(school_id: int, db: Session = Depends(get_db)):
    db_school = school_crud.delete_school(db, school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school

@router.put("/{school_id}", response_model=SchoolOut)
def update(school_id: int, school: SchoolCreate, db: Session = Depends(get_db)):
    db_school = school_crud.update_school(db, school_id, school)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school
