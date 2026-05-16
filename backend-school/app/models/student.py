# app/models/student.py
from sqlalchemy import Column, String, Date, Boolean
from app.db.session import Base  # ✅ Import de la classe Base

class Student(Base):  # ✅ Héritage simple, PAS d'arguments
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    enrollment_date = Column(Date, nullable=False)
    is_synced = Column(Boolean, default=False)