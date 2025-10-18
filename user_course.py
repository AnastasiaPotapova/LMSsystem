from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("sqlite:///users.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class UserCourse(Base):
    __tablename__ = "users_course"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return f"<UserCourse(id={self.id}, user_id={self.user_id}, course_id={self.course_id})>"

# Создание таблицы
Base.metadata.create_all(engine)

class UserCourseManager:
    def __init__(self):
        self.session = Session()

    def post(self, user_id, course_id):
        """Добавить связку пользователь-курс"""
        user_course = UserCourse(user_id=user_id, course_id=course_id)
        self.session.add(user_course)
        try:
            self.session.commit()
            print(f"[OK] связь пользователя {user_id} с курсом {course_id} добавлена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, user_course_id):
        """Получить связь по id"""
        return self.session.query(UserCourse).filter_by(id=user_course_id).first()

    def get_all(self):
        """Получить все связи"""
        return self.session.query(UserCourse).all()

    def get_by_user(self, user_id):
        """Получить все курсы пользователя"""
        return self.session.query(UserCourse).filter_by(user_id=user_id).all()

    def edit(self, user_course_id, new_user_id=None, new_course_id=None):
        """Редактировать связь"""
        user_course = self.get(user_course_id)
        if not user_course:
            print("[ERR] Связь не найдена")
            return

        if new_user_id:
            user_course.user_id = new_user_id
        if new_course_id:
            user_course.course_id = new_course_id

        try:
            self.session.commit()
            print(f"[OK] Связь {user_course_id} обновлена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, user_course_id):
        """Удалить связь по id связи"""
        user_course = self.get(user_course_id)
        if not user_course:
            print("[ERR] Связь не найдена")
            return

        self.session.delete(user_course)
        self.session.commit()
        print(f"[OK] Связь {user_course_id} удалена")

    def delete_by_ids(self, user_id, course_id):
        """Удалить связь по user_id и course_id"""
        user_course = self.session.query(UserCourse).filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()

        if not user_course:
            print("[ERR] Связь не найдена")
            return

        self.session.delete(user_course)
        self.session.commit()
        print(f"[OK] Связь пользователя {user_id} с курсом {course_id} удалена")
