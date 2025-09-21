from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Transactions API",
    description="A simple API to manage financial transactions for DevSecOps testing.",
    version="1.0.0"
)

# --- Dependência para obter a sessão do banco de dados ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints CRUD ---

@app.post("/transactions/", response_model=schemas.Transaction, tags=["Transactions"])
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a new financial transaction.
    """
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[schemas.Transaction], tags=["Transactions"])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all transactions with pagination.
    """
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single transaction by its ID.
    """
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def update_transaction(transaction_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Update an existing transaction.
    """
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
        
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Delete a transaction by its ID.
    """
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return db_transaction

# Endpoint de exemplo para teste do SAST (propositalmente inseguro)
@app.get("/transactions/search/", tags=["Transactions"])
def search_transactions(q: str, db: Session = Depends(get_db)):
    """
    [INSECURE] Search for transactions by description. 
    This endpoint uses raw SQL and is vulnerable to SQL Injection. For SAST testing only.
    """
    # ATENÇÃO: A linha abaixo é propositalmente insegura para testes de SAST.
    # NUNCA use f-strings ou formatação de string para construir queries SQL.
    query = f"SELECT * FROM transactions WHERE description LIKE '%{q}%'"
    
    # A maneira correta seria usar parâmetros de consulta seguros:
    # query = "SELECT * FROM transactions WHERE description LIKE :query"
    # result = db.execute(query, {"query": f"%{q}%"}).fetchall()
    
    result = db.execute(query).fetchall()
    return result