from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("sqlite:///users.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    author = Column(String, default='unknown')
    is_published = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title}, author={self.author})>"

# Создание таблицы
Base.metadata.create_all(engine)

class CourseManager:
    def __init__(self):
        self.session = Session()

    def post(self, title, description="", author="unknown"):
        """Добавить курс"""
        course = Course(title=title, description=description, author=author)
        self.session.add(course)
        try:
            self.session.commit()
            print(f"[OK] Курс '{title}' добавлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, course_id):
        """Получить курс по id"""
        return self.session.query(Course).filter_by(id=course_id).first()

    def get_all(self):
        """Получить все курсы"""
        return self.session.query(Course).all()

    def edit(self, course_id, new_title=None, new_description=None, new_author=None, new_is_published=None):
        """Редактировать курс"""
        course = self.get(course_id)
        if not course:
            print("[ERR] Курс не найден")
            return

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
            print(f"[OK] Курс {course_id} обновлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, course_id):
        """Удалить курс"""
        course = self.get(course_id)
        if not course:
            print("[ERR] Курс не найден")
            return
        self.session.delete(course)
        try:
            self.session.commit()
            print(f"[OK] Курс {course_id} удален")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

# Создаем тестовые курсы при импорте
def create_test_courses():
    """Создает тестовые курсы если их нет"""
    manager = CourseManager()
    existing_courses = manager.get_all()
    
    if len(existing_courses) == 0:
        test_courses = [
            {"title": "Математика", "description": "Основы математики", "author": "Профессор Иванов"},
            {"title": "Программирование", "description": "Python для начинающих", "author": "Доцент Петров"},
            {"title": "Базы данных", "description": "SQL и SQLAlchemy", "author": "Преподаватель Сидоров"}
        ]
        
        for course_data in test_courses:
            manager.post(
                title=course_data["title"],
                description=course_data["description"],
                author=course_data["author"]
            )
        print("[OK] Созданы тестовые курсы")

create_test_courses()