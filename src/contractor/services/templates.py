"""模板渲染服务：加载并渲染合同模板"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape, DebugUndefined
from ..utils.paths import TEMPLATE_DIR

# 初始化 Jinja2 环境，设置加载器与自动转义
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(enabled_extensions=("tex", "j2",)),
    undefined=DebugUndefined,
)


def render_template(template_file: str, context: dict) -> str:
    """渲染指定模板文件"""
    # 获取模板并渲染上下文
    template = _env.get_template(template_file)
    return template.render(**context)


def available_templates() -> list[str]:
    """列出可用的合同模板"""
    # 搜索符合命名规则的模板文件
    files = Path(TEMPLATE_DIR).glob("contract_*.tex.j2")
    return sorted(
        p.name.removeprefix("contract_").removesuffix(".tex.j2") for p in files
    )
