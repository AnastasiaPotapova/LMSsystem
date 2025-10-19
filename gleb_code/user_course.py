from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.exc import IntegrityError
from database import Base, Session

class UserCourse(Base):
    __tablename__ = "users_course"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return f"<UserCourse(id={self.id}, user_id={self.user_id}, course_id={self.course_id})>"

class UserCourseManager:
    def __init__(self):
        self.session = Session()

    def post(self, user_id, course_id):
        """Добавить связку пользователь-курс"""
        user_course = UserCourse(user_id=user_id, course_id=course_id)
        self.session.add(user_course)
        try:
            self.session.commit()
            print(f"[OK] Пользователь {user_id} успешно записан на курс {course_id}")
            return True
        except IntegrityError:
            self.session.rollback()
            print(f"[ERROR] Пользователь {user_id} или курс {course_id} не существует")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось записать пользователя на курс: {e}")
            return False

    def get(self, user_course_id):
        """Получить связь по id"""
        user_course = self.session.query(UserCourse).filter_by(id=user_course_id).first()
        if not user_course:
            print(f"[ERROR] Связь с ID {user_course_id} не найдена")
        return user_course

    def get_all(self):
        """Получить все связи"""
        return self.session.query(UserCourse).all()

    def get_by_user(self, user_id):
        """Получить все курсы пользователя"""
        user_courses = self.session.query(UserCourse).filter_by(user_id=user_id).all()
        if not user_courses:
            print(f"[INFO] Пользователь {user_id} не записан ни на один курс")
        return user_courses

    def edit(self, user_course_id, new_user_id=None, new_course_id=None):
        """Редактировать связь"""
        user_course = self.get(user_course_id)
        if not user_course:
            print(f"[ERROR] Связь с ID {user_course_id} не найдена")
            return False

        if new_user_id:
            user_course.user_id = new_user_id
        if new_course_id:
            user_course.course_id = new_course_id

        try:
            self.session.commit()
            print(f"[OK] Связь {user_course_id} успешно обновлена")
            return True
        except IntegrityError:
            self.session.rollback()
            print(f"[ERROR] Пользователь {new_user_id} или курс {new_course_id} не существует")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось обновить связь: {e}")
            return False

    def delete(self, user_course_id):
        """Удалить связь по id связи"""
        user_course = self.get(user_course_id)
        if not user_course:
            print(f"[ERROR] Связь с ID {user_course_id} не найдена")
            return False

        self.session.delete(user_course)
        try:
            self.session.commit()
            print(f"[OK] Связь {user_course_id} успешно удалена")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось удалить связь: {e}")
            return False

    def delete_by_ids(self, user_id, course_id):
        """Удалить связь по user_id и course_id"""
        user_course = self.session.query(UserCourse).filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()

        if not user_course:
            print(f"[ERROR] Связь пользователя {user_id} с курсом {course_id} не найдена")
            return False

        self.session.delete(user_course)
        try:
            self.session.commit()
            print(f"[OK] Пользователь {user_id} успешно отписан от курса {course_id}")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось отписать пользователя от курса: {e}")
            return False