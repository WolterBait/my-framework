from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    amount = Column(Float, unique=True)
    term_months = Column(Integer, unique=True)
    balance = Column(Float, unique=True)
    created_at = Column(DateTime, nullable=False)

    # Первое значение       | Тип данных столбца
    # primary_key=True      | Этот столбец — первичный ключ
    # ForeignKey('user.id') | Этот столбец — внешний ключ (с чем связан)

    # autoincrement=True    | При добавлении новой записи значение в этом столбце будет автоматически присвоено БД
    # unique=True           | Поле обязательно для заполнения
    # nullable=False        | Значение поля должны быть уникальными