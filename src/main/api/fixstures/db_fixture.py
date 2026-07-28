import pytest
from src.main.api.db.engine import SessionLocal, engine

@pytest.fixture(scope="function")
def db_session():
    """
    Фикстура, предоставляющая сессию базы данных для тестов.
    ВСЕ изменения, сделанные в тесте, будут автоматически откатаны
    (rollback) после завершения теста – даже если тест упадёт с ошибкой.
    Это сделает наши тесты чистыми и повторяемыми.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


























