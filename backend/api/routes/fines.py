from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.crud import get_fines_by_student, pay_fine
from backend.api.dependencies import get_db
from backend.api.routes.auth import get_current_admin  # Import JWT Protection

router = APIRouter()

# ✅ 9. GET fines for a student (Only for Admins)
@router.get("/{student_id}")
def get_student_fines(student_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    fines = get_fines_by_student(db, student_id)
    return {"fines": fines}

# ✅ 10. PUT - Pay a fine (Only for Admins)
@router.put("/pay/{fine_id}")
def pay_student_fine(fine_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    updated_fine = pay_fine(db, fine_id)
    if not updated_fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return {"message": "Fine paid successfully", "fine": updated_fine}
