from sqlalchemy import Column, Integer, String, Float, Date, Enum
from database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, default="Uncategorized")
    transaction_type = Column(Enum(TransactionType), nullable=False)