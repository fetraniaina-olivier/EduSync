# app/models/__init__.py
"""
Registre central des modèles SQLAlchemy.
L'import ici est CRUCIAL : il force SQLAlchemy à connaître toutes les classes
avant de tenter de résoudre les relations (ex: School <-> SyncOperation).
"""
from app.models.base import Base
from app.models.school import School
from app.models.user import User
from app.models.sync_operation import SyncOperation
from app.models.student import Student  # ✅ Ajout
from app.models.teacher import Teacher  # ✅ Ajout

__all__ = ["Base", "School", "User", "SyncOperation", "Student", "Teacher"]