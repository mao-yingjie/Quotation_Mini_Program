# 测试模板渲染及默认值行为
from contractor.services.templates import render_template, available_templates


def fake_money_str(amount_minor: int, code: str, locale: str) -> str:
    """模拟货币格式化函数"""
    return f"{amount_minor/100:.2f} {code}"


# 构造基础上下文字典
base_context = {
    "title": "Sample Contract",
    "version": "0.1",
    "document_id": "doc1",
    "party": {"name": "Alice"},
    "counterparty": {"name": "Bob"},
    "amount": {"value": 1000, "currency": "USD"},
    "money_str": fake_money_str,
    "payment_terms": "Net 30",
    "delivery_terms": "Email",
    "ipr_confidentiality": "NDA",
    "dispute_resolution": "Law",
    "others": "None",
    "scope": "Consulting",
}


def test_available_templates_has_english_template():
    """验证英文模板可被发现"""
    assert "basic_en" in available_templates()


def test_missing_country_defaults():
    """缺失国家信息时应使用默认值"""
    ctx = base_context.copy()
    rendered = render_template("contract_basic_en.tex.j2", ctx)
    assert "Alice (US)" in rendered
    assert "Bob (US)" in rendered


def test_missing_variable_placeholder():
    """缺失字段应提示占位符"""
    ctx = base_context.copy()
    ctx.pop("scope")
    rendered = render_template("contract_basic_en.tex.j2", ctx)
    assert "Undefined" in rendered
    assert "scope" in rendered
