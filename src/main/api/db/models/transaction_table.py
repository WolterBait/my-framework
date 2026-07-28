from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from src.main.api.db.base import Base



class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    from_account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    credit_id = Column(Integer, ForeignKey('credit.id'), unique=False, nullable=False)
    amount = Column(Float, unique=False)
    transaction_type = Column(String, unique=False)
    created_at = Column(DateTime, nullable=False)

    # Первое значение       | Тип данных столбца
    # primary_key=True      | Этот столбец — первичный ключ
    # ForeignKey('user.id') | Этот столбец — внешний ключ (с чем связан)

    # autoincrement=True    | При добавлении новой записи значение в этом столбце будет автоматически присвоено БД
    # unique=True           | Поле обязательно для заполнения
    # nullable=False        | Значение поля должны быть уникальными