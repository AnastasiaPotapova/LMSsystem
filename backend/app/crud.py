from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models
from .auth import pwd_context


# ----------------------------------------------------------
# USERS
# ----------------------------------------------------------

def create_user(db: Session, username: str, password_hash: str, role=models.RoleEnum.admin):
    user = models.User(username=username, hashed_password=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session):
    return db.query(models.User).all()


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"ok": True}


# ----------------------------------------------------------
# COURSES
# ----------------------------------------------------------

def list_courses(db: Session):
    return db.query(models.Course).all()


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def create_course(db: Session, title: str, description: str = ""):
    c = models.Course(title=title, description=description)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def delete_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course:
        db.delete(course)
        db.commit()


# ----------------------------------------------------------
# CHAPTERS
# ----------------------------------------------------------

def list_chapters(db: Session):
    """Возвращает все главы."""
    return db.query(models.Chapter).all()


def get_chapter(db: Session, chapter_id: int):
    """Возвращает одну главу по ID."""
    return db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()


def create_chapter(db: Session, title: str, course_id: int):
    """Создаёт новую главу, связанную с курсом."""
    ch = models.Chapter(title=title, course_id=course_id)
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


def delete_chapter(db: Session, chapter_id: int):
    ch = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if ch:
        db.delete(ch)
        db.commit()


# ----------------------------------------------------------
# LESSONS
# ----------------------------------------------------------

def create_lesson(db: Session, title: str, content: str, chapter_id: int | None = None):
    l = models.Lesson(title=title, content=content, chapter_id=chapter_id)
    db.add(l)
    db.commit()
    db.refresh(l)
    return l

def update_lesson_content(db: Session, lesson_id: int, content: str):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        return None
    lesson.content = content
    db.commit()
    db.refresh(lesson)
    return lesson

def list_lessons(db: Session):
    return db.query(models.Lesson).all()


def get_lesson(db: Session, lesson_id: int):
    """Возвращает одну главу по ID."""
    return db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()

# ----------------------------------------------------------
# TASKS
# ----------------------------------------------------------

def create_task(db: Session, title: str, description: str, chapter_id: int):
    task = models.Task(title=title, description=description, chapter_id=chapter_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    """Возвращает одну главу по ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def list_tasks(db: Session):
    return db.query(models.Task).all()


# ----------------------------------------------------------
# ENROLLMENTS
# ----------------------------------------------------------

def enroll_user(db: Session, user_id: int, course_id: int):
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    if existing:
        return existing
    e = models.Enrollment(user_id=user_id, course_id=course_id)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


# ----------------------------------------------------------
# SUBMISSIONS
# ----------------------------------------------------------

def submit_task(db: Session, user_id: int, task_id: int, content: str, status=models.SubmissionStatus.partial):
    s = db.query(models.Submission).filter(
        models.Submission.user_id == user_id,
        models.Submission.task_id == task_id
    ).first()
    if s:
        s.content = content
        s.status = status
        db.commit()
        db.refresh(s)
        return s
    s = models.Submission(user_id=user_id, task_id=task_id, content=content, status=status)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def create_user_admin(db: Session, username: str, password: str, role: models.RoleEnum):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    hashed_pw = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user