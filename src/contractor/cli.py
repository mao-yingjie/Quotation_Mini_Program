# CLI 命令模块：提供合作方、合同及报表的命令行操作
"""合同管理的命令行工具，提供合作方管理、合同生成与报表等功能。"""

# 导入标准库与第三方库
import os, json, yaml
from pathlib import Path
from datetime import date
import typer
from rich import print
from rich.table import Table
from sqlmodel import select
from .db import init_db, get_session
from .models import Party, Contract, ContractFile
from .services.templates import available_templates
from .services.render import render_tex, compile_pdf
from .services.converter import tex_to_docx
from .services.versioning import commit_all
from .services.reports import totals_by_partner, totals_by_period, export_csv
from .utils.paths import ROOT, CONTRACTS_DIR

# 创建 Typer 应用
app = typer.Typer(add_completion=False, help="Contractor CLI")


@app.command("init-db")
def init_db_cmd():
    """初始化数据库"""
    # 调用数据库初始化函数
    init_db()
    print("[green]Database initialized.[/green]")

@app.command("party-add")
def party_add(name: str, country: str = typer.Option(None)):
    """添加新的合作方"""
    with get_session() as s:
        # 创建并保存合作方
        p = Party(name=name, country=country)
        s.add(p)
        s.commit()
        s.refresh(p)
        print(f"[cyan]Party created with id={p.id}[/cyan]")


@app.command("party-list")
def party_list(
    json_out: bool = typer.Option(False, "--json", help="输出 JSON 数据"),
):
    """列出所有合作方"""
    # 从数据库读取合作方
    with get_session() as s:
        parties = s.exec(select(Party)).all()
    if json_out:
        # 输出 JSON 结构化数据
        data = [p.model_dump() for p in parties]
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        # 使用 rich.table 以表格形式展示
        table = Table(title="Parties")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Country")
        for p in parties:
            table.add_row(str(p.id), p.name, p.country or "")
        print(table)

@app.command("template-list")
def template_list():
    """列出所有可用的合同模板"""
    # 遍历模板生成器输出模板名称
    for t in available_templates():
        print("-", t)

@app.command("contract-new")
def contract_new(
    template: str = typer.Option("basic_zh", "--template"),
    data: Path = typer.Option(..., "--data", exists=True, file_okay=True),
    version: str = "0.1.0",
    outdir: Path = typer.Option(Path("contracts"), "--outdir", file_okay=False),
):
    """创建新合同并渲染对应模板"""
    # 读取 YAML 数据生成上下文
    ctx = yaml.safe_load(data.read_text(encoding="utf-8"))
    party_name = ctx.get("party", {}).get("name", "Unknown")
    with get_session() as s:
        # 查找或创建合作方
        party = s.exec(select(Party).where(Party.name == party_name)).first()
        if not party:
            party = Party(name=party_name, country=ctx.get("party", {}).get("country"))
            s.add(party); s.commit(); s.refresh(party)
        # 将金额转换为最小货币单位
        amount_minor = int(round(float(ctx.get("amount", {}).get("value", 0.0)) * 100))
        # 创建合同记录
        c = Contract(
            title=ctx.get("title", "Untitled Contract"),
            party_id=party.id,
            currency=ctx.get("amount", {}).get("currency", "CNY"),
            amount_minor=amount_minor,
            version=version,
            template_name=template,
            status="draft",
        )
        s.add(c); s.commit(); s.refresh(c)
        # 渲染 LaTeX 模板并保存路径
        doc_id = f"contract_{c.id}_v{c.version}"
        outdir = outdir / str(c.id)
        tex_path = render_tex(
            f"contract_{template}.tex.j2", ctx | {"document_id": doc_id}, outdir
        )
        s.add(ContractFile(contract_id=c.id, kind="tex", path=str(tex_path)))
        s.commit()
        print(
            f"[green]Contract {c.id} created and .tex rendered at {tex_path}[/green]"
        )

@app.command("contract-render")
def contract_render(
    id: int = typer.Option(..., "--id"),
    pdf: bool = typer.Option(False, "--pdf"),
    docx: bool = typer.Option(False, "--docx"),
):
    """将合同渲染为 PDF 或 DOCX"""
    engine = os.getenv("LATEX_ENGINE", "tectonic")
    with get_session() as s:
        # 获取合同并检查存在性
        c = s.get(Contract, id)
        if not c:
            print("[red]Contract not found[/red]"); raise typer.Exit(1)
        outdir = Path("contracts") / str(c.id)
        tex_path = outdir / f"contract_{c.id}_v{c.version}.tex"
        if not tex_path.exists():
            print("[yellow].tex not found. Nothing to render.[/yellow]"); raise typer.Exit(1)
        if pdf:
            # 编译为 PDF
            pdf_path = compile_pdf(tex_path, engine=engine)
            if pdf_path:
                s.add(ContractFile(contract_id=id, kind="pdf", path=str(pdf_path)))
                s.commit()
                print(f"[green]PDF created: {pdf_path}[/green]")
        if docx:
            # 转换为 DOCX
            docx_path = tex_to_docx(tex_path)
            if docx_path:
                s.add(ContractFile(contract_id=id, kind="docx", path=str(docx_path)))
                s.commit()
                print(f"[green]DOCX created: {docx_path}[/green]")


@app.command("contract-list")
def contract_list(
    party_id: int = typer.Option(None, "--party-id", help="按合作方过滤"),
    json_out: bool = typer.Option(False, "--json", help="输出 JSON 数据"),
):
    """列出合同信息"""
    with get_session() as s:
        # 构建查询语句，支持按合作方过滤
        stmt = select(Contract)
        if party_id is not None:
            stmt = stmt.where(Contract.party_id == party_id)
        contracts = s.exec(stmt).all()
    if json_out:
        # 输出 JSON 数据
        data = []
        for c in contracts:
            item = c.model_dump()
            item["party_name"] = c.party.name if c.party else None
            data.append(item)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        # 以表格形式展示合同
        table = Table(title="Contracts")
        table.add_column("ID", justify="right")
        table.add_column("Title")
        table.add_column("Party")
        table.add_column("Status")
        table.add_column("Version")
        for c in contracts:
            table.add_row(
                str(c.id),
                c.title,
                c.party.name if c.party else "",
                c.status,
                c.version,
            )
        print(table)


@app.command("contract-update")
def contract_update(
    id: int = typer.Argument(..., help="合同 ID"),
    title: str | None = typer.Option(None, "--title", help="更新标题"),
    status: str | None = typer.Option(None, "--status", help="更新状态"),
    effective_date: date | None = typer.Option(
        None, "--effective-date", formats=["%Y-%m-%d"], help="生效日期"
    ),
    json_out: bool = typer.Option(False, "--json", help="输出 JSON 数据"),
):
    """更新合同信息"""
    with get_session() as s:
        # 查询并更新合同
        c = s.get(Contract, id)
        if not c:
            print("[red]Contract not found[/red]"); raise typer.Exit(1)
        if title is not None:
            c.title = title
        if status is not None:
            c.status = status
            c.status_history.append(status)
        if effective_date is not None:
            c.effective_date = effective_date
        s.add(c); s.commit(); s.refresh(c)
        if json_out:
            # 输出 JSON 数据
            data = c.model_dump()
            data["party_name"] = c.party.name if c.party else None
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            # 表格展示更新后的结果
            table = Table(title=f"Contract {c.id}")
            table.add_column("Field")
            table.add_column("Value")
            table.add_row("Title", c.title)
            table.add_row("Party", c.party.name if c.party else "")
            table.add_row("Status", c.status)
            table.add_row("Version", c.version)
            table.add_row(
                "Effective Date",
                c.effective_date.isoformat() if c.effective_date else "",
            )
            print(table)

@app.command("report-totals")
def report_totals(currency: str = "CNY"):
    """按合作方统计合同金额"""
    totals = totals_by_partner(currency=currency)  # 汇总金额
    print(json.dumps(totals, ensure_ascii=False, indent=2))  # 输出结果


@app.command("reports")
def reports_cmd(
    kind: str = typer.Option("partner", "--kind", help="partner or period"),
    fmt: str = typer.Option("html", "--format", help="html or csv"),
    out: Path | None = typer.Option(
        None, "--out", file_okay=True, dir_okay=False, help="输出文件路径"
    ),
    currency: str = typer.Option("CNY", "--currency"),
):
    """生成报表并以 HTML 或 CSV 输出"""
    # 根据不同维度生成汇总数据
    if kind == "period":
        totals = totals_by_period(currency=currency)
        title = "Totals by Period"
    else:
        totals = totals_by_partner(currency=currency)
        title = "Totals by Partner"
    # 根据输出格式生成文件或直接打印
    if fmt == "csv":
        path = out or Path(f"{kind}_report.csv")
        export_csv(totals, path)
        print(f"[green]CSV written to {path}[/green]")
    else:
        rows = "\n".join(
            f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in totals.items()
        )
        html = (
            f"<html><head><meta charset='utf-8'><title>{title}</title></head>"
            f"<body><table>{rows}</table></body></html>"
        )
        if out:
            out.write_text(html, encoding="utf-8")
            print(f"[green]HTML written to {out}[/green]")
        else:
            print(html)

@app.command("repo-commit")
def repo_commit(message: str = typer.Option("Update artifacts")):
    """提交生成的合同文件到 Git 仓库"""
    ok = commit_all(Path.cwd(), message)
    print(
        "[green]Committed.[/green]" if ok else "[yellow]Nothing to commit or git failed.[/yellow]"
    )

if __name__ == "__main__":
    # 入口函数
    app()
