from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Student


class StudentRepository:

    async def get_by_id(
        self, db: AsyncSession, student_id: int
    ):
        return await db.get(Student, student_id)

    async def get_by_email(
        self, db: AsyncSession, email: str
    ):
        result = await db.scalars(
            select(Student).where(Student.email == email)
        )
        return result.first()

    async def create(
        self, db: AsyncSession, data: dict
    ):
        student = Student(**data)
        db.add(student)
        await db.flush()
        return student

    async def list_students(
        self,
        db: AsyncSession,
        page: int,
        limit: int,
    ):
        total = await db.scalar(
            select(func.count()).select_from(Student)
        )

        stmt = (
            select(Student)
            .order_by(Student.id)
            .offset((page - 1) * limit)
            .limit(limit)
        )

        result = await db.scalars(stmt)

        return result.all(), total or 0

    async def delete(
        self, db: AsyncSession, student: Student
    ):
        await db.delete(student)