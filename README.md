<!-- 文件作用：介绍项目、快速开始、常见问题与开发者文档链接 -->

# Contractor — Python Contract Automation (LaTeX → PDF & Word)

Authoring in **LaTeX (with Jinja2)**, producing **PDF** via Tectonic/XeLaTeX and **Word (.docx)** via **Pandoc**.

## Quick Start (openSUSE)
```bash
# 安装依赖并初始化数据库
sudo zypper install tectonic
sudo zypper install pandoc
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
contractor init-db
contractor contract new --template basic_zh --data data/sample_contract.yml --outdir contracts
contractor contract render --id 1 --pdf --docx
```

## CLI 使用示例

以下命令展示了常见的工作流程：

```bash
# 常见工作流程示例：列出模板、添加合作方并生成合同
# 列出可用模板
contractor template-list

# 添加合作方
contractor party-add --name "ACME" --country "CN"

# 创建并渲染合同
contractor contract-new --template basic_zh --data data/sample_contract.yml --outdir contracts
contractor contract-render --id 1 --pdf --docx
```

## 合同生成演示

运行上方 CLI 示例即可生成并查看合同效果。

## FAQ

**Q: 生成 PDF 失败怎么办？**  \
A: 请确认已安装 Tectonic/XeLaTeX，并在 `PATH` 中可用。

**Q: 如何切换到 Word 输出？**  \
A: 在 `contract-render` 命令中加上 `--docx` 参数即可。

**Q: 数据库文件存放在哪里？**  \
A: 默认使用项目根目录下的 `contractor.db`，可在环境变量中自定义路径。

**Q: 如何自定义输出目录？**  \
A: 在 `contract-new` 和 `contract-render` 命令中使用 `--outdir` 参数指定保存位置。

## 开发者文档

更多开发相关信息可参阅 [`docs/`](docs/) 目录：

- [系统架构](docs/architecture.md)
- [代码风格](docs/code_style.md)
- [贡献流程](docs/contributing.md)

