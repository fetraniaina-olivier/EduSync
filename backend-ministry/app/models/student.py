# app/models/student.py
from sqlalchemy import String, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Student(Base):
    __tablename__ = "students"
    
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[str | None] = mapped_column(String(10), nullable=True)  # YYYY-MM-DD
    enrollment_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    
    __table_args__ = (
        Index("idx_student_school", "school_id"),
        Index("idx_student_name", "last_name", "first_name"),
    )
    
    school = relationship("School", back_populates="students")
    
    def __repr__(self):
        return f"<Student(id='{self.id}', name='{self.first_name} {self.last_name}')>"