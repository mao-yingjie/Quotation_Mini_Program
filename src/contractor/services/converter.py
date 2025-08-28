"""转换服务：利用 Pandoc 将 LaTeX 文件转换为其他格式"""

import subprocess
from pathlib import Path


def tex_to_docx(tex_path: Path, reference_docx: Path | None = None) -> Path | None:
    """将 tex 文件转换为 docx，可选引用模板"""
    # 构造输出 docx 路径
    docx_path = tex_path.with_suffix(".docx")
    # 组装 Pandoc 基本命令
    cmd = ["pandoc", str(tex_path), "-o", str(docx_path)]
    # 如提供参考文档且存在，则用于保持样式
    if reference_docx and reference_docx.exists():
        cmd.extend(["--reference-doc", str(reference_docx)])
    try:
        # 调用 Pandoc 执行转换
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 如果生成成功则返回路径
        return docx_path if docx_path.exists() else None
    except Exception as e:
        # 捕获异常并给出警告
        print(f"[WARN] Pandoc conversion failed: {e}")
        return None


def tex_to_html(tex_path: Path) -> Path | None:
    """将 tex 文件转换为 html"""
    # 构造输出 html 路径
    html_path = tex_path.with_suffix(".html")
    # 组装 Pandoc 命令并启用独立模式
    cmd = ["pandoc", str(tex_path), "-s", "-o", str(html_path)]
    try:
        # 执行转换
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 返回生成的 html 文件路径
        return html_path if html_path.exists() else None
    except Exception as e:
        # 捕获异常并给出警告
        print(f"[WARN] Pandoc conversion failed: {e}")
        return None
