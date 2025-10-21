from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("sqlite:///task.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    exercise = Column(String, primary_key=True)


    def __repr__(self):
        return f"<Lesson(id={self.id}, name={self.theme}, exercise={self.text})>"


# Создаем таблицу
Base.metadata.create_all(engine)


class TaskManager:
    def __init__(self):
        self.session = Session()

    def post(self, name, exercise):
        """Добавить задание"""
        task = Task(name=name, exercise=exercise)
        self.session.add(task)
        try:
            self.session.commit()
            print(f"[OK] Урок {id} добавлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, task_id):
        """Получить задание по id"""
        return self.session.query(Task).filter_by(id=task_id).first()

    def get_all(self):
        """Получить все задания"""
        return self.session.query(Task).all()

    def edit(self, task_id, new_name=None, new_exercise=None):
        """Редактировать задание"""
        task = self.get(task_id)
        if not task:
            print("[ERR] Задание не найдено")
            return
        if new_name:
            task.name = new_name
        if new_exercise:
            task.exercise = new_exercise
        try:
            self.session.commit()
            print(f"[OK] Задание {task_id} обновлено")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, task_id):
        """Удалить задание"""
        task = self.get(task_id)
        if not task:
            print("[ERR] Задание не найдено")
            return
        self.session.delete(task)
        try:
            self.session.commit()
            print(f"[OK] Задание {task_id} удалено")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)