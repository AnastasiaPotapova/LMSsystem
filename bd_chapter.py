from sqlalchemy import create_engine, Column, Integer, ARRAY
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

    def edit(self, id, new_id=None):
        """Редактировать id"""
        chapter = self.get(id)
        if not chapter:
            print("[ERR] Глава не найдена")
            return False
        if new_role:
            chapter.id = new_id
        try:
            self.session.commit()
            print(f"[OK] Глава {id} обновлена")
            return True
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)
            return False

    def add_lesson(self, ch, lessonc):
        """Добавить урок (содержание) к главе"""
        chapter = self.get(ch)
        if not chapter:
            print("[ERR] Глава не найдена")
            return

        # Если массив уроков пуст, создаем новый массив
        if chapter.lesson is None:
            chapter.lesson = [lessonc]
        else:
            # Добавляем урок в существующий массив
            chapter.lesson = list(chapter.lesson) + [lessonc]

        try:
            self.session.commit()
            print(f"[OK] Урок '{lessonc}' добавлен к главе")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def add_task(self, ch, taskc):
        """Добавить задание (содержание) к главе"""
        chapter = self.get(ch)
        if not chapter:
            print("[ERR] Глава не найдена")
            return

        # Если массив заданий пуст, создаем новый массив
        if chapter.task is None:
            chapter.task = [taskc]
        else:
            # Добавляем задание в существующий массив
            chapter.task = list(chapter.task) + [taskc]

        try:
            self.session.commit()
            print(f"[OK] Задание '{taskc}' добавлено к главе")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)
