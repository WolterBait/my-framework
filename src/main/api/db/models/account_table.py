from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.main.api.db.base import Base

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    number = Column(String, unique=True ,nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Account(id={self.id}, user_id={self.user_id}, number={self.number}), balance={self.balance})>"

# Первое значение       | Тип данных столбца
# primary_key=True      | Этот столбец — первичный ключ
# ForeignKey('user.id') | Этот столбец — внешний ключ (с чем связан)

# autoincrement=True    | При добавлении новой записи значение в этом столбце будет автоматически присвоено БД
# unique=True           | Поле обязательно для заполнения
# nullable=False        | Значение поля должны быть уникальными