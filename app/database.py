from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o caminho e nome do arquivo do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"

# Cria o "motor" de conexão do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM (mapeamento objeto-relacional)
Base = declarative_base()