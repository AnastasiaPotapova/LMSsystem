
from sqlalchemy import create_engine, Column, Integer, ARRAY #ээээээ
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("sqlite:///chapter.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True)
    lesson = Column(ARRAY, primary_key=True)
    task = Column(ARRAY, primary_key=True)


    def __repr__(self):
        return f"<Chapter(id={self.id}, lesson={self.lesson}, task={self.task})>"


# Создаем таблицу
Base.metadata.create_all(engine)


class ChapterManager:
    def __init__(self):
        self.session = Session()

    def post(self, task, lesson):
        """Добавить связь"""
        chap = Chapter(task=task, lesson=lesson)
        self.session.add(chap)
        try:
            self.session.commit()
            print(f"[OK] Связь {task} и {lesson} добавлена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, id):
        """Получить главу по id"""
        return self.session.query(Chapter).filter_by(id=id).first()

    def get_all(self):
        """Получить все главы"""
        return self.session.query(Chapter).all()

    def edit(self, id, new_role=None):
        """Редактировать id"""
        chapter = self.get(id)
        if not chapter:
            print("[ERR] Глава не найдена")
            return
        if new_role:
            chapter.role = new_role

        try:
            self.session.commit()
            print(f"[OK] Глава {id} обновлена")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, id):
        """Удалить главу"""
        chapter = self.get(id)
        if not chapter:
            print("[ERR] Глава не найдена")
            return
        self.session.delete(chapter)
        self.session.commit()
        print(f"[OK] Глава {id} удалена")

    def add_lesson(self):
        ...

    def add_task(self):
        ...

