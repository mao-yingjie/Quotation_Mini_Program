"""批量写入示例 Party 和 Contract 数据的脚本"""

from __future__ import annotations

from pathlib import Path
import sys

# 确保 src 目录在导入路径中
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from contractor.db import init_db, get_session
from contractor.models import Party, Contract


def seed() -> None:
    """向数据库填充示例的 Party 和 Contract 记录"""
    init_db()

    parties = [
        Party(name="Alpha Corp", country="CN"),
        Party(name="Beta LLC", country="US"),
    ]

    with get_session() as session:
        session.add_all(parties)
        session.commit()

        contracts = [
            Contract(
                title="Alpha Master Agreement",
                party_id=parties[0].id,
                currency="CNY",
                amount_minor=100_00,
                status_history=["draft"],
                currency_rate=1.0,
            ),
            Contract(
                title="Beta Service Contract",
                party_id=parties[1].id,
                currency="USD",
                amount_minor=200_00,
                status_history=["draft"],
                currency_rate=7.0,
            ),
        ]
        session.add_all(contracts)
        session.commit()


if __name__ == "__main__":
    seed()
