
import subprocess
from pathlib import Path
from typing import Optional
from .templates import render_template
from ..utils.paths import CONTRACTS_DIR

def render_tex(template_file: str, context: dict, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    tex = render_template(template_file, context)
    tex_path = outdir / f"{context.get('document_id', 'contract')}.tex"
    tex_path.write_text(tex, encoding="utf-8")
    return tex_path

def compile_pdf(tex_path: Path, engine: str = "tectonic") -> Optional[Path]:
    cwd = tex_path.parent
    if engine == "tectonic":
        cmd = ["tectonic", str(tex_path.name), "--keep-logs"]
    elif engine == "xelatex":
        cmd = ["xelatex", "-interaction=nonstopmode", str(tex_path.name)]
    else:
        raise ValueError("Unknown LaTeX engine")
    try:
        subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print(f"[WARN] LaTeX compile failed: {e}")
        return None
    pdf_path = tex_path.with_suffix(".pdf")
    return pdf_path if pdf_path.exists() else None
