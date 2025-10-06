from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("sqlite:///users.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False, default='user')
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, role={self.role}, email={self.email})>"


# Создаем таблицу
Base.metadata.create_all(engine)


class UserManager:
    def __init__(self):
        self.session = Session()

    def post(self, email, password, role='user'):
        """Добавить пользователя"""
        user = User(role=role, email=email, password=password)
        self.session.add(user)
        try:
            self.session.commit()
            print(f"[OK] Пользователь {email} добавлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def get(self, user_id):
        """Получить пользователя по id"""
        return self.session.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email):
        """Получить пользователя по email"""
        return self.session.query(User).filter_by(email=email).first()

    def get_all(self):
        """Получить всех пользователей"""
        return self.session.query(User).all()

    def edit(self, user_id, new_role=None, new_email=None, new_password=None):
        """Редактировать пользователя"""
        user = self.get(user_id)
        if not user:
            print("[ERR] Пользователь не найден")
            return
        if new_role:
            user.role = new_role
        if new_email:
            user.email = new_email
        if new_password:
            user.password = new_password
        try:
            self.session.commit()
            print(f"[OK] Пользователь {user_id} обновлен")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)

    def delete(self, user_id):
        """Удалить пользователя"""
        user = self.get(user_id)
        if not user:
            print("[ERR] Пользователь не найден")
            return
        self.session.delete(user)
        try:
            self.session.commit()
            print(f"[OK] Пользователь {user_id} удален")
        except Exception as e:
            self.session.rollback()
            print("[ERR]", e)


# Пример использования
if __name__ == "__main__":
    manager = UserManager()
    
    # Добавляем пользователей
    manager.post("admin@mail.com", "admin123", "admin")
    manager.post("user@mail.com", "password123")
    
    # Получаем всех пользователей
    users = manager.get_all()
    print("Все пользователи:")
    for user in users:
        print(user)
    
    # Обновляем пользователя
    manager.edit(1, new_role="superadmin")
    
    # Ищем по email
    user = manager.get_by_email("user@mail.com")
    print(f"Найден по email: {user}")