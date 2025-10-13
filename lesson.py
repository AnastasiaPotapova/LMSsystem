
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("sqlite:///lesson.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True)
    theme = Column(String, primary_key=True)
    text = Column(String, primary_key=True)


    def __repr__(self):
        return f"<Lesson(id={self.id}, theme={self.theme}, text={self.text})>"


# Создаем таблицу
Base.metadata.create_all(engine)


class LessonManager:
    def __init__(self):
        self.session = Session()

    def post(self, theme, text):
        """Добавить урок"""
        lesson = Lesson(theme=theme, text=text)
        self.session.add(lesson)
        try:
            self.session.commit()
            print(f"[OK] Урок {id} добавлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, lesson_id):
        """Получить урок по id"""
        return self.session.query(Lesson).filter_by(id=lesson_id).first()

    def get_all(self):
        """Получить все уроки"""
        return self.session.query(Lesson).all()

    def edit(self, lesson_id, new_theme=None, new_text=None):
        """Редактировать урок"""
        lesson = self.get(lesson_id)
        if not lesson:
            print("[ERR] Урок не найден")
            return
        if new_theme:
            lesson.theme = new_theme
        if new_text:
            lesson.text = new_text
        try:
            self.session.commit()
            print(f"[OK] Урок {lesson_id} обновлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, lesson_id):
        """Удалить урок"""
        lesson = self.get(lesson_id)
        if not lesson:
            print("[ERR] Урок не найден")
            return
        self.session.delete(lesson)
        try:
            self.session.commit()
            print(f"[OK] Урок {lesson_id} удален")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)