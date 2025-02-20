from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.crud import get_fines_by_student, pay_fine
from backend.api.dependencies import get_db

router = APIRouter()

# ✅ 9. GET fines for a student
@router.get("/{student_id}")
def get_student_fines(student_id: int, db: Session = Depends(get_db)):
    fines = get_fines_by_student(db, student_id)
    return {"fines": fines}

# ✅ 10. PUT - Pay a fine
@router.put("/pay/{fine_id}")
def pay_student_fine(fine_id: int, db: Session = Depends(get_db)):
    updated_fine = pay_fine(db, fine_id)
    if not updated_fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return {"message": "Fine paid successfully", "fine": updated_fine}
