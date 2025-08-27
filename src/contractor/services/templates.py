
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..utils.paths import TEMPLATE_DIR

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(enabled_extensions=("tex", "j2",))
)

def render_template(template_file: str, context: dict) -> str:
    template = _env.get_template(template_file)
    return template.render(**context)

def available_templates() -> list[str]:
    return [p.name for p in Path(TEMPLATE_DIR).glob("*.j2")]
