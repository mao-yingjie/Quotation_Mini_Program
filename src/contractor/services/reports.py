
# 报表服务模块：提供合同金额的汇总与导出功能
"""汇总合同金额并支持导出为多种格式。"""

from __future__ import annotations

from pathlib import Path
import csv
from sqlmodel import select
from ..db import get_session
from ..models import Contract, Party
from .currency import money_str, convert_minor

def totals_by_partner(currency: str = "CNY") -> dict[str, str]:
    """按合作方汇总合同金额"""
    with get_session() as s:
        # 查询合作方及其合同金额
        rows = s.exec(
            select(Party.name, Contract.amount_minor, Contract.currency).join(Contract)
        ).all()
    totals: dict[str, int] = {}
    for name, amt, cur in rows:
        if cur != currency:
            amt = convert_minor(amt, cur, currency)  # 若币种不同则转换
        totals[name] = totals.get(name, 0) + amt  # 累加金额
    return {k: money_str(v, currency) for k, v in totals.items()}


def totals_by_period(currency: str = "CNY") -> dict[str, str]:
    """按月份汇总合同金额"""
    with get_session() as s:
        # 查询合同的生效日期及金额
        rows = s.exec(
            select(Contract.effective_date, Contract.amount_minor, Contract.currency)
        ).all()
    totals: dict[str, int] = {}
    for dt, amt, cur in rows:
        if not dt:
            continue  # 未指定日期的合同忽略
        key = dt.strftime("%Y-%m")
        if cur != currency:
            amt = convert_minor(amt, cur, currency)  # 统一币种
        totals[key] = totals.get(key, 0) + amt
    return {k: money_str(v, currency) for k, v in sorted(totals.items())}


def export_csv(totals: dict[str, str], path: Path) -> Path:
    """将汇总结果导出为 CSV 文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "total"])  # 写入表头
        for name, total in totals.items():
            writer.writerow([name, total])  # 写入每行数据
    return path
