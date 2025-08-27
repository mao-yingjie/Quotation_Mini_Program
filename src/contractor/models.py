
from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Party(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    country: Optional[str] = None
    contracts: List["Contract"] = Relationship(back_populates="party")

class Contract(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    party_id: int = Field(foreign_key="party.id")
    currency: str = "CNY"
    amount_minor: int = 0  # store as minor units (e.g., cents)
    version: str = "0.1.0"
    template_name: str = "basic_zh"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    effective_date: Optional[date] = None
    status: str = "draft"

    party: Party = Relationship(back_populates="contracts")
    files: List["ContractFile"] = Relationship(back_populates="contract")

class ContractFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contract_id: int = Field(foreign_key="contract.id")
    kind: str  # "tex" | "pdf" | "docx"
    path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    contract: Contract = Relationship(back_populates="files")
