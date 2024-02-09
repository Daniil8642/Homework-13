# auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import User, create_access_token, verify_password, get_current_user  # Исправлен импорт

router = APIRouter()

def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# Реєстрація нового користувача
@router.post("/register/", response_model=User)
def register_user(username: str, password: str, db: Session = Depends(get_db_session)):
    # Перевірка, чи користувач з таким ім'ям користувача вже існує
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач з таким ім'ям вже існує")

    # Створення нового користувача
    new_user = User(username=username, hashed_password=verify_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Авторизація користувача та отримання токену доступу
@router.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db_session)):
    # Пошук користувача за ім'ям користувача
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильне ім'я користувача або пароль")

    # Створення токену доступу
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# Отримання інформації про поточного користувача
@router.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
# auth.py
