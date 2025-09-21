from pydantic import BaseModel
from datetime import date
from models import TransactionType

# Schema base com os campos comuns
class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float
    category: str
    transaction_type: TransactionType

# Schema para a criação de uma nova transação (não precisa de ID)
class TransactionCreate(TransactionBase):
    pass

# Schema para a leitura de uma transação (inclui o ID)
class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de objetos ORM