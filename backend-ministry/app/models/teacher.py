# app/models/teacher.py
from sqlalchemy import String, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Teacher(Base):
    __tablename__ = "teachers"
    
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hire_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    school_id: Mapped[str] = mapped_column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    
    __table_args__ = (Index("idx_teacher_school", "school_id"),)
    
    school = relationship("School", back_populates="teachers")
    
    def __repr__(self):
        return f"<Teacher(id='{self.id}', name='{self.first_name} {self.last_name}')>"