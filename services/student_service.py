from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.student_repository import StudentRepository
from schemas import StudentCreate, StudentUpdate


class StudentNotFound(Exception):
    pass


class EmailAlreadyExists(Exception):
    pass


class InvalidStudentData(Exception):
    pass


class StudentService:

    def __init__(self):
        self.repo = StudentRepository()

    async def create_student(
        self, db: AsyncSession, data: StudentCreate
    ):
        if await self.repo.get_by_email(db, str(data.email)):
            raise EmailAlreadyExists()

        try:
            student = await self.repo.create( 
                db, data.model_dump()       # dictionaty representation of the model.
            )
            await db.commit()
            await db.refresh(student)
            return student

        except IntegrityError as exc:
            await db.rollback()
            raise EmailAlreadyExists() from exc

        except Exception:
            await db.rollback()
            raise

    async def update_student(
        self,
        db: AsyncSession,
        student_id: int,
        data: StudentUpdate,
    ):
        student = await self.repo.get_by_id(db, student_id)

        if student is None:
            raise StudentNotFound()

        changes = data.model_dump(exclude_unset=True)

        if not changes:
            raise InvalidStudentData("Provide at least one field to update")

        if any(value is None for value in changes.values()):
            raise InvalidStudentData("Fields cannot be null")

        if "email" in changes:
            existing = await self.repo.get_by_email(
                db, str(changes["email"])
            )
            if existing and existing.id != student_id:
                raise EmailAlreadyExists()

        try:
            for field, value in changes.items():
                setattr(student, field, value)

            await db.commit()
            await db.refresh(student)
            return student

        except IntegrityError as exc:
            await db.rollback()
            raise EmailAlreadyExists() from exc

        except Exception:
            await db.rollback()
            raise

    async def delete_student(
        self, db: AsyncSession, student_id: int
    ):
        student = await self.repo.get_by_id(db, student_id)

        if student is None:
            raise StudentNotFound()

        try:
            await self.repo.delete(db, student)
            await db.commit()

        except Exception:
            await db.rollback()
            raise

    async def list_students(
        self,
        db: AsyncSession,
        page: int,
        limit: int,
    ):
        items, total = await self.repo.list_students(
            db, page, limit
        )

        return {
            "items": items,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        }