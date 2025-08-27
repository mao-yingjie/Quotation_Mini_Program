
import subprocess
from pathlib import Path
from ..utils.paths import PANDOC_DIR

def tex_to_docx(tex_path: Path, reference_docx: Path | None = None) -> Path | None:
    docx_path = tex_path.with_suffix(".docx")
    cmd = ["pandoc", str(tex_path), "-o", str(docx_path)]
    ref = reference_docx if reference_docx and reference_docx.exists() else (PANDOC_DIR / "docx-reference.docx")
    if ref.exists():
        cmd.extend(["--reference-doc", str(ref)])
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return docx_path if docx_path.exists() else None
    except Exception as e:
        print(f"[WARN] Pandoc conversion failed: {e}")
        return None
