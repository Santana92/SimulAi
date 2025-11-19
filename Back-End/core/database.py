from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import DATABASE_URL

# Cria a engine de conexão assíncrona com o banco de dados
engine = create_async_engine(DATABASE_URL, echo=True)

# Cria uma fábrica de sessões assíncronas
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base declarativa para os modelos ORM
Base = declarative_base()

# Dependência para obter uma sessão do banco de dados em cada requisição
async def get_db():
    async with SessionLocal() as session:
        yield session
