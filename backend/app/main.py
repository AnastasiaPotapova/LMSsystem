from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models, database, auth, crud
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Minimal LMS API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # фронт на Vite
        "http://127.0.0.1:5173",  # иногда используется эта форма
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# AUTH
# -------------------------------
@app.post('/register')
def register(username: str, password: str, db: Session = Depends(auth.get_db)):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail='User already exists')
    hashed = auth.get_password_hash(password)
    role = models.RoleEnum.admin
    user = crud.create_user(db, username, hashed, role)
    return {"id": user.id, "username": user.username, "role": user.role.value}


@app.post('/token')
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(auth.get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value}


# -------------------------------
# PUBLIC ROUTES
# -------------------------------
@app.get('/courses')
def list_courses(db: Session = Depends(auth.get_db)):
    return crud.list_courses(db)


@app.get('/courses/{course_id}')
def get_course(course_id: int, db: Session = Depends(auth.get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


# -------------------------------
# USER ROUTES
# -------------------------------
@app.post('/courses/{course_id}/enroll')
def enroll_in_course(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    return crud.enroll_user(db, current_user.id, course_id)


@app.get('/courses/{course_id}/lessons')
def list_lessons(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    return crud.list_lessons(db, course_id, current_user.id)


@app.get('/tasks/{task_id}')
def get_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


@app.post('/tasks/{task_id}/submit')
def submit_task(
    task_id: int,
    solution: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    return crud.submit_task(db, current_user.id, task_id, solution)

@app.get('/tasks')
def list_tasks(db: Session = Depends(auth.get_db)):
    return crud.list_tasks(db)


@app.get('/lessons')
def list_courses(db: Session = Depends(auth.get_db)):
    return crud.list_lessons(db)


@app.get('/lessons/{lesson_id}')
def get_lesson(
    lesson_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')
    return lesson

# -------------------------------
# ADMIN ROUTES
# -------------------------------
# ---------------- Courses ----------------
@app.post('/admin/courses')
def create_course(
    title: str,
    description: str = "",
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    return crud.create_course(db, title, description)


@app.delete('/admin/courses/{course_id}')
def delete_course(
    course_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    crud.delete_course(db, course_id)
    return {"status": "deleted", "course_id": course_id}


# ---------------- Chapters ----------------
@app.post('/admin/chapters')
def create_chapter(
    title: str,
    course_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    return crud.create_chapter(db, title, course_id)


@app.delete('/admin/chapters/{chapter_id}')
def delete_chapter(
    chapter_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    crud.delete_chapter(db, chapter_id)
    return {"status": "deleted", "chapter_id": chapter_id}


# ---------------- Lessons ----------------

class LessonUpdate(BaseModel):
    content: str

@app.post('/admin/lessons')
def create_lesson(
    title: str,
    content: str,
    chapter_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    return crud.create_lesson(db, title, content, chapter_id)


@app.delete('/admin/lessons/{lesson_id}')
def delete_lesson(
    lesson_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    crud.delete_lesson(db, lesson_id)
    return {"status": "deleted", "lesson_id": lesson_id}


@app.put("/lessons/{lesson_id}")
def update_lesson(
    lesson_id: int,
    update: LessonUpdate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    lesson = crud.update_lesson_content(db, lesson_id, update.content)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

# ---------------- Tasks/Assignments ----------------
class TaskCreate(BaseModel):
    title: str
    description: str = ''
    chapter_id: int

@app.post('/admin/tasks')
def create_task(
    task: TaskCreate,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    return crud.create_task(db, task.title, task.description, task.chapter_id)


@app.delete('/admin/tasks/{task_id}')
def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    crud.delete_task(db, task_id)
    return {"status": "deleted", "task_id": task_id}

class TaskUpdate(BaseModel):
    content: str

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate,
                db: Session = Depends(auth.get_db),
                current_admin: dict = Depends(auth.get_current_admin)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.content = task_update.content
    db.commit()
    db.refresh(task)
    return {"message": "Task updated successfully", "task": {"id": task.id, "title": task.title}}

# ---------------- List endpoints ----------------
@app.get('/admin/courses')
def list_courses(
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    return crud.list_courses(db)


@app.get('/admin/chapters')
def list_chapters(
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    return crud.list_chapters(db)


@app.get('/admin/lessons')
def list_lessons(
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    return crud.list_lessons(db)


@app.get('/admin/tasks')
def list_tasks(
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    return crud.list_tasks(db)

@app.get('/admin/users')
def list_users(
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    return crud.list_users(db)

@app.post("/admin/users")
def create_user(
    username: str,
    password: str,
    role: models.RoleEnum,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    return crud.create_user_admin(db, username, password, role)


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(auth.get_db)
):
    return crud.delete_user(db, user_id)


@app.get("/")
def root():
    return {"message": "Minimal LMS API is running"}
