from pydantic import BaseModel
from datetime import date

class StudentCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    birth_date: date
    enrollment_date: date

class StudentOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    birth_date: date
    enrollment_date: date
    is_synced: bool

    class Config:
        from_attributes = True