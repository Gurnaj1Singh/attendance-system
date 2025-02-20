from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.crud import get_notifications, send_notification, mark_notification_as_read
from backend.api.dependencies import get_db
from pydantic import BaseModel

router = APIRouter()

# ✅ Pydantic model for creating a notification
class NotificationCreate(BaseModel):
    student_id: int
    message: str

# ✅ 11. GET notifications for a student
@router.get("/{student_id}")
def get_student_notifications(student_id: int, db: Session = Depends(get_db)):
    notifications = get_notifications(db, student_id)
    return {"notifications": notifications}

# ✅ 12. POST - Send a notification
@router.post("/")
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = send_notification(db, notification.student_id, notification.message)
    return {"message": "Notification sent successfully", "notification": new_notification}

# ✅ 13. PUT - Mark a notification as read
@router.put("/read/{notification_id}")
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    updated_notification = mark_notification_as_read(db, notification_id)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read", "notification": updated_notification}
