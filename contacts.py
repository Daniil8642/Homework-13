# contacts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Contact, ContactCreate, User, get_current_user

router = APIRouter()

# Залежність для отримання сесії бази даних
def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# Отримання контактів для поточного користувача
@router.get("/contacts/", response_model=list[Contact])
def get_user_contacts(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    contacts = db.query(Contact).filter(Contact.owner_id == current_user.id).all()
    return contacts

# Створення нового контакту
@router.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# Оновлення контакту
@router.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact_update: ContactCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    existing_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()

    if existing_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")

    for field, value in contact_update.dict().items():
        setattr(existing_contact, field, value)

    db.commit()
    db.refresh(existing_contact)
    return existing_contact

# Видалення контакту
@router.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()

    if contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")

    db.delete(contact)
    db.commit()

    return contact
# contacts.py
