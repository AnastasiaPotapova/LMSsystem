from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import IntegrityError
from database import Base, Session  # Импортируем из общего файла

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    author = Column(String, default='unknown')
    is_published = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title}, author={self.author})>"

class CourseManager:
    def __init__(self):
        self.session = Session()

    def post(self, title, description="", author="unknown"):
        """Добавить курс"""
        course = Course(title=title, description=description, author=author)
        self.session.add(course)
        try:
            self.session.commit()
            print(f"[OK] Курс '{title}' успешно создан")
            return True
        except IntegrityError:
            self.session.rollback()
            print(f"[ERROR] Курс с названием '{title}' уже существует")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось создать курс: {e}")
            return False

    def get(self, course_id):
        """Получить курс по id"""
        course = self.session.query(Course).filter_by(id=course_id).first()
        if not course:
            print(f"[ERROR] Курс с ID {course_id} не найден")
        return course

    def get_all(self):
        """Получить все курсы"""
        return self.session.query(Course).all()

    def edit(self, course_id, new_title=None, new_description=None, new_author=None, new_is_published=None):
        """Редактировать курс"""
        course = self.get(course_id)
        if not course:
            print(f"[ERROR] Курс с ID {course_id} не найден")
            return False

        # Применяем изменения
        if new_title:
            course.title = new_title
        if new_description:
            course.description = new_description
        if new_author:
            course.author = new_author
        if new_is_published is not None:
            course.is_published = new_is_published

        try:
            self.session.commit()
            print(f"[OK] Курс {course_id} успешно обновлен")
            return True
        except IntegrityError:
            self.session.rollback()
            print(f"[ERROR] Курс с названием '{new_title}' уже существует")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось обновить курс: {e}")
            return False

    def delete(self, course_id):
        """Удалить курс"""
        course = self.get(course_id)
        if not course:
            print(f"[ERROR] Курс с ID {course_id} не найден")
            return False

        self.session.delete(course)
        try:
            self.session.commit()
            print(f"[OK] Курс {course_id} успешно удален")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось удалить курс: {e}")
            return False