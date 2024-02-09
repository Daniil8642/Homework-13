# models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date
from .database import Base
from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
