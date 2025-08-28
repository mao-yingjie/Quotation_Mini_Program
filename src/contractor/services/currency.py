
# 汇率工具模块：负责获取、缓存并转换每日汇率
"""提供汇率获取、缓存与金额转换的辅助函数。"""

from __future__ import annotations

from babel.numbers import format_currency
from moneyed import Money, get_currency
from num2words import num2words

from datetime import date
from pathlib import Path
import json
from urllib.request import urlopen

RATES_FILE = Path("data") / "exchange_rates.json"  # 缓存汇率数据的文件路径


def _load_rates() -> dict:
    """加载本地缓存的汇率数据"""
    if RATES_FILE.exists():
        try:
            return json.loads(RATES_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save_rates(data: dict) -> None:
    """将汇率数据写入本地缓存"""
    RATES_FILE.parent.mkdir(parents=True, exist_ok=True)
    RATES_FILE.write_text(json.dumps(data))


def _get_rates(base: str) -> dict[str, float]:
    """获取指定基础货币的汇率并进行每日缓存"""
    cache = _load_rates()  # 读取缓存数据
    today = date.today().isoformat()
    if base in cache and cache[base].get("date") == today:
        return cache[base]["rates"]  # 当日已缓存则直接返回
    url = f"https://open.er-api.com/v6/latest/{base}"  # 无需 API Key 的汇率接口
    try:
        with urlopen(url, timeout=10) as resp:  # nosec B310
            data = json.loads(resp.read())
            rates = data.get("rates", {})
    except Exception:
        rates = {}
    cache[base] = {"date": today, "rates": rates}  # 更新缓存
    _save_rates(cache)
    return rates


def exchange_rate(from_code: str, to_code: str) -> float:
    """获取两种货币之间的汇率"""
    if from_code == to_code:
        return 1.0  # 同币种无需转换
    rates = _get_rates(from_code)
    return float(rates.get(to_code, 1.0))


def convert_minor(amount_minor: int, from_code: str, to_code: str) -> int:
    """按当前汇率转换最小单位金额"""
    rate = exchange_rate(from_code, to_code)
    return int(round(amount_minor * rate))

def as_money_minor(amount_minor: int, code: str = "CNY") -> Money:
    """将最小单位金额转换为 Money 对象"""
    cur = get_currency(code)
    return Money(amount_minor / 100, cur)

def money_str(amount_minor: int, code: str = "CNY", locale: str = "zh_CN") -> str:
    """格式化金额为本地化的字符串"""
    m = as_money_minor(amount_minor, code)
    return format_currency(m.amount, m.currency.code, locale=locale)
