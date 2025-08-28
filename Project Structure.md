# 项目结构
```
contractor-starter/
├─ pyproject.toml                 # 依赖与可执行入口（contractor 命令）
├─ README.md                      # openSUSE 安装与快速开始
├─ .env.example                   # 环境变量示例（DB/引擎等）
├─ src/contractor/
│  ├─ cli.py                      # Typer 命令：init-db/new/render/report/repo-commit
│  ├─ db.py                       # SQLite 引擎与会话
│  ├─ models.py                   # Party/Contract/ContractFile ORM
│  ├─ services/
│  │  ├─ templates.py             # Jinja2 模板加载/渲染
│  │  ├─ render.py                # 渲染 .tex + 调用 tectonic/xelatex 产 PDF
│  │  ├─ converter.py             # 调用 pandoc 将 .tex → .docx
│  │  ├─ versioning.py            # Git 自动提交（可选）
│  │  ├─ reports.py               # 金额汇总（按合作方）
│  │  └─ currency.py              # 金额格式化（Babel/moneyed 等）
│  └─ utils/paths.py              # 路径常量
├─ templates/
│  ├─ latex/
│  │  ├─ base.tex                 # 公共排版（XeCJK，适配中文）
│  │  └─ contract_basic_zh.tex.j2 # 示例合同（Jinja2 + LaTeX）
│  └─ pandoc/                     # 可选：存放 Word 样式参考 docx
├─ data/
│  └─ sample_contract.yml         # 示例数据（甲乙方、金额、条款等）
├─ contracts/                     # 生成产物输出目录（按ID分文件夹）
├─ scripts/ensure_tools.sh        # 检查 tectonic/pandoc 是否安装
└─ tests/test_smoke.py            # 烟囱测试
