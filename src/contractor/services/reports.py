
from sqlmodel import select
from ..db import get_session
from ..models import Contract, Party
from .currency import money_str

def totals_by_partner(currency: str = "CNY"):
    with get_session() as s:
        rows = s.exec(select(Party.name, Contract.amount_minor).join(Contract)).all()
    totals = {}
    for name, amt in rows:
        totals[name] = totals.get(name, 0) + amt
    return {k: money_str(v, currency) for k, v in totals.items()}
