from fastapi import APIRouter, Depends, HTTPException
from server.schemas import UserRegistration, LoginRequest
from server.crud.users import add_new_user, get_user_by_email, verify_password
import server.models as md
from server.utils import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/register')
def register_user(user: UserRegistration, session: Session = Depends(get_db)):
    db_user = md.User(username=user.username, email=user.email, password=user.password)
    new_user = add_new_user(db_user, session)
    return new_user


@router.post('/login')
def login(user_data: LoginRequest, session: Session = Depends(get_db)):
    user = get_user_by_email(user_data.email, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}
