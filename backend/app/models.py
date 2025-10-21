from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.types import DateTime
import enum


# ----------------------------------------------------------
# ENUMS
# ----------------------------------------------------------

class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"


class SubmissionStatus(enum.Enum):
    not_solved = "not_solved"
    partial = "partial"
    done = "done"


# ----------------------------------------------------------
# USER
# ----------------------------------------------------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)

    enrollments = relationship('Enrollment', back_populates='user')
    submissions = relationship('Submission', back_populates='user')


# ----------------------------------------------------------
# COURSE
# ----------------------------------------------------------

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")

    chapters = relationship('Chapter', back_populates='course', cascade="all, delete-orphan")


# ----------------------------------------------------------
# CHAPTER
# ----------------------------------------------------------

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="chapters")
    lessons = relationship("Lesson", back_populates="chapter", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="chapter", cascade="all, delete-orphan")


# ----------------------------------------------------------
# LESSON
# ----------------------------------------------------------

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, default="")
    chapter_id = Column(Integer, ForeignKey('chapters.id'))

    chapter = relationship('Chapter', back_populates='lessons')


# ----------------------------------------------------------
# TASK
# ----------------------------------------------------------

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)

    chapter = relationship("Chapter", back_populates="tasks")
    submissions = relationship(
        "Submission", back_populates="task", cascade="all, delete-orphan"
    )


# ----------------------------------------------------------
# ENROLLMENT
# ----------------------------------------------------------

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    user = relationship('User', back_populates='enrollments')
    course = relationship('Course')


# ----------------------------------------------------------
# SUBMISSION
# ----------------------------------------------------------

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    content = Column(Text, default="")
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.not_solved)

    user = relationship('User', back_populates='submissions')
    task = relationship('Task', back_populates='submissions')
