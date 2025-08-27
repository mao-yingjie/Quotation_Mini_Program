
from babel.numbers import format_currency
from moneyed import Money, get_currency
from num2words import num2words

def as_money_minor(amount_minor: int, code: str = "CNY") -> Money:
    cur = get_currency(code)
    return Money(amount_minor / 100, cur)

def money_str(amount_minor: int, code: str = "CNY", locale: str = "zh_CN") -> str:
    m = as_money_minor(amount_minor, code)
    return format_currency(m.amount, m.currency.code, locale=locale)
