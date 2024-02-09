# utils.py
from datetime import datetime
from typing import List

def get_current_datetime():
    return datetime.now()

def format_birthdays(birthdays: List[datetime]):
    formatted_birthdays = [birthday.strftime("%Y-%m-%d") for birthday in birthdays]
    return formatted_birthdays

def send_email(subject: str, body: str, to_email: str, from_email: str, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str):
    #код для відправлення електронної пошти
    pass
# utils.py
