from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

# Cria a engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL, echo=True)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter uma sessão do banco de dados em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
