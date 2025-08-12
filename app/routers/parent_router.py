from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import parent_schema
from app.crud import parent_crud
from app.database import get_db

router = APIRouter(prefix="/parents", tags=["Parents"])


@router.post("/", response_model=parent_schema.ParentOut)
def create_parent(parent: parent_schema.ParentCreate, db: Session = Depends(get_db)):
    result = parent_crud.create_parent(db, parent)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{parent_id}", response_model=parent_schema.ParentOut)
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    parent = parent_crud.get_parent(db, parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.get("/", response_model=list[parent_schema.ParentOut])
def read_parents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return parent_crud.get_parents(db, skip, limit)

@router.put("/{parent_id}", response_model=parent_schema.ParentOut)
def update_parent(parent_id: int, update_data: parent_schema.ParentCreate, db: Session = Depends(get_db)):
    result = parent_crud.update_parent(db, parent_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Parent not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{parent_id}", response_model=parent_schema.ParentOut)
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    parent = parent_crud.delete_parent(db, parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent
