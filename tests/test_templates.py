"""测试模板渲染与默认值逻辑。"""

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
    # 调用模板列表函数并检查是否存在英文模板
    assert "basic_en" in available_templates()


def test_missing_country_defaults():
    """缺失国家信息时应使用默认值"""
    # 复制基础上下文并渲染模板
    ctx = base_context.copy()
    rendered = render_template("contract_basic_en.tex.j2", ctx)
    # 验证渲染结果中使用默认国家代码
    assert "Alice (US)" in rendered
    assert "Bob (US)" in rendered


def test_missing_variable_placeholder():
    """缺失字段应提示占位符"""
    # 删除上下文中的关键字段以模拟缺失
    ctx = base_context.copy()
    ctx.pop("scope")
    # 渲染模板并检查占位符提示
    rendered = render_template("contract_basic_en.tex.j2", ctx)
    assert "Undefined" in rendered
    assert "scope" in rendered

from contractor.services.render import render_tex


def test_render_tex_writes_file(tmp_path):
    """渲染 LaTeX 模板并写出包含合同信息的文件"""
    # 复制上下文并指定文档编号
    ctx = base_context.copy()
    ctx["document_id"] = "demo"
    # 调用 render_tex 生成 TeX 文件
    tex_path = render_tex("contract_basic_en.tex.j2", ctx, tmp_path)
    # 读取生成的文件并验证内容
    content = tex_path.read_text(encoding="utf-8")
    assert tex_path.exists()
    assert "Sample Contract" in content
    assert "Alice (US)" in content
