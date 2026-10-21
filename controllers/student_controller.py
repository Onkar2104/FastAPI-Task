from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas import StudentCreate, StudentUpdate, StudentResponse, StudentPage
from services.student_service import (
    StudentService,
    StudentNotFound,
    EmailAlreadyExists,
    InvalidStudentData,
)

router = APIRouter(prefix="/students", tags=["Students"])
service = StudentService()


def handle_service_error(exc: Exception):
    if isinstance(exc, StudentNotFound):
        raise HTTPException(404, "Student not found")

    if isinstance(exc, EmailAlreadyExists):
        raise HTTPException(409, "Email already exists")

    if isinstance(exc, InvalidStudentData):
        raise HTTPException(400, str(exc))

    raise exc


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    data: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.create_student(db, data)
    except (StudentNotFound, EmailAlreadyExists, InvalidStudentData) as exc:
        handle_service_error(exc)


@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.update_student(db, student_id, data)
    except (StudentNotFound, EmailAlreadyExists, InvalidStudentData) as exc:
        handle_service_error(exc)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        await service.delete_student(db, student_id)
    except (StudentNotFound, EmailAlreadyExists, InvalidStudentData) as exc:
        handle_service_error(exc)


@router.get("/", response_model=StudentPage)
async def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_students(db, page, limit)