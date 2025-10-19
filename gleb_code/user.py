from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from database import Base, Session

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False, default='user')
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, role={self.role}, email={self.email})>"

class UserManager:
    def __init__(self):
        self.session = Session()

    def post(self, email, password, role='user'):
        """Добавить пользователя"""
        user = User(role=role, email=email, password=password)
        self.session.add(user)
        try:
            self.session.commit()
            print(f"[OK] Пользователь '{email}' успешно создан")
            return True
        except IntegrityError:
            self.session.rollback()
            print(f"[ERROR] Пользователь с email '{email}' уже существует")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось создать пользователя: {e}")
            return False

    def get(self, user_id):
        """Получить пользователя по id"""
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"[ERROR] Пользователь с ID {user_id} не найден")
        return user

    def get_by_email(self, email):
        """Получить пользователя по email"""
        user = self.session.query(User).filter_by(email=email).first()
        if not user:
            print(f"[ERROR] Пользователь с email '{email}' не найден")
        return user

    def get_all(self):
        """Получить всех пользователей"""
        return self.session.query(User).all()

    def edit(self, user_id, new_role=None, new_email=None, new_password=None):
        """Редактировать пользователя"""
        user = self.get(user_id)
        if not user:
            print(f"[ERROR] Пользователь с ID {user_id} не найден")
            return False

        # Применяем изменения
        if new_role:
            user.role = new_role
        if new_email:
            user.email = new_email
        if new_password:
            user.password = new_password

        try:
            self.session.commit()
            print(f"[OK] Пользователь {user_id} успешно обновлен")
            return True
        except IntegrityError:
            self.session.rollback()
            print(f"[ERROR] Email '{new_email}' уже используется другим пользователем")
            return False
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось обновить пользователя: {e}")
            return False

    def delete(self, user_id):
        """Удалить пользователя"""
        user = self.get(user_id)
        if not user:
            print(f"[ERROR] Пользователь с ID {user_id} не найден")
            return False

        self.session.delete(user)
        try:
            self.session.commit()
            print(f"[OK] Пользователь {user_id} успешно удален")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"[ERROR] Не удалось удалить пользователя: {e}")
            return False