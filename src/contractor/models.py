"""定义 Party、Contract 与 ContractFile 数据模型"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, JSON
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
    amount_minor: int = 0  # 以最小货币单位存储（例如分）
    version: str = "0.1.0"
    template_name: str = "basic_zh"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    effective_date: Optional[date] = None
    status: str = "draft"
    status_history: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    currency_rate: float = 1.0

    party: Party = Relationship(back_populates="contracts")
    files: List["ContractFile"] = Relationship(back_populates="contract")

class ContractFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contract_id: int = Field(foreign_key="contract.id")
    kind: str  # 文件类型: "tex" | "pdf" | "docx"
    path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    contract: Contract = Relationship(back_populates="files")
