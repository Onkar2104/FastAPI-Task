from sqlalchemy.orm import Session
from models import Student
from schemas import StudentCreate, StudentUpdate


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(db: Session, student: StudentCreate):
    new_student = Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(
    db: Session,
    student_id: int,
    student: StudentUpdate
):
    existing_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not existing_student:
        return None

    existing_student.name = student.name
    existing_student.email = student.email
    existing_student.course = student.course

    db.commit()
    db.refresh(existing_student)

    return existing_student


def delete_student(db: Session, student_id: int):
    existing_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not existing_student:
        return None

    db.delete(existing_student)
    db.commit()

    return existing_student