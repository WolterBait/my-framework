from sqlalchemy.orm import Session
from src.main.api.db.models.account_table import Account


class AccountCrudDb:
    @staticmethod # Статик метод, чтобы не создавать экземпляр класса
                  # в самом тесте, а сразу через класс обращаться
    def get_account_by_id (db: Session, account_id: int) -> Account | None:
        """
        Выполняет поиск аккаунта в БД по его ID.
        db — это сессия SQLAlchemy (приходит из фикстуры db_session).
        account_id — ID, полученный из ответа API (response.id).
        Он возвращает объект Account или None, если запись не найдена
        В тесте вы передаёте db_session и response.id, чтобы проверить, что аккаунт действительно создался в БД.
        """
        return db.query(Account).filter_by(id=account_id).first()


    @staticmethod
    def count_all(db: Session) -> int:
        """Возвращает общее количество аккаунтов в БД."""
        return db.query(Account).count()

