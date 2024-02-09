# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import contacts, auth, user

app: FastAPI = FastAPI() 

# Налаштування CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Додавання роутерів
app.include_router(contacts.router)
app.include_router(auth.router)
app.include_router(user.router)
# main.py
