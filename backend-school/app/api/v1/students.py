from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentOut

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=StudentOut, status_code=201)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Student).where(Student.id == data.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="ID étudiant déjà utilisé")

    student = Student(**data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

@router.get("/", response_model=list[StudentOut])
async def get_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).order_by(Student.last_name))
    return result.scalars().all()