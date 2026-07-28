from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.main.api.db.base import Base

class User(Base):
    __tablename__ = 'user'  # Имя таблицы в БД
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role}), delete_at={self.delete_at})>"

    # Первое значение    | Тип данных столбца
    # primary_key=True   | Этот столбец — первичный ключ
    # autoincrement=True | При добавлении новой записи значение в этом столбце будет автоматически присвоено БД
    # unique=True        | Поле обязательно для заполнения
    # nullable=False     | Значение поля должны быть уникальными






















