# database.py
import os
import asyncpg
from typing import Optional, List, Any
import logging
from contextlib import asynccontextmanager
from pydantic import BaseConfig
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """Создание пула подключений"""
        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            self.logger.info("Database connection pool created successfully")
        except Exception as e:
            self.logger.error(f"Error creating database connection pool: {e}")
            raise

    async def disconnect(self):
        """Закрытие пула подключений"""
        if self.pool:
            await self.pool.close()
            self.logger.info("Database connection pool closed")

    @asynccontextmanager
    async def get_connection(self):
        """Контекстный менеджер для получения подключения"""
        if not self.pool:
            raise RuntimeError("Database connection pool is not initialized")
        
        connection = await self.pool.acquire()
        try:
            yield connection
        finally:
            await self.pool.release(connection)

    async def execute(self, query: str, *args) -> str:
        """Выполнение запроса без возврата результата"""
        async with self.get_connection() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> List[asyncpg.Record]:
        """Выполнение SELECT запроса с возвратом всех строк"""
        async with self.get_connection() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Выполнение SELECT запроса с возвратом одной строки"""
        async with self.get_connection() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Any:
        """Выполнение SELECT запроса с возвратом одного значения"""
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)

    async def execute_many(self, query: str, args_list: List[tuple]) -> None:
        """Массовое выполнение запроса"""
        async with self.get_connection() as conn:
            await conn.executemany(query, args_list)

class DatabaseConfig(BaseConfig):
    """Конфигурация базы данных"""
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("POSTGRES_DB", "comet_db")
    db_user: str = os.getenv("POSTGRES_USER", "postgres")
    db_password: str = os.getenv("POSTGRES_PASS", "password")
    
    class Config:
        env_file = ".env"

    @property
    def dsn(self) -> str:
        """Формирование DSN строки для asyncpg"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
class PostgresDB(Database):
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        super().__init__(self.config.dsn)
    
    async def health_check(self) -> bool:
        """Проверка подключения к БД"""
        try:
            async with self.get_connection() as conn:
                result = await conn.fetchval("SELECT 1")
                return result == 1
        except Exception:
            return False

# Global database instance
db = PostgresDB()