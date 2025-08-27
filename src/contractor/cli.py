
import os, json, yaml
from pathlib import Path
import typer
from rich import print
from sqlmodel import select
from .db import init_db, get_session
from .models import Party, Contract, ContractFile
from .services.templates import available_templates
from .services.render import render_tex, compile_pdf
from .services.converter import tex_to_docx
from .services.versioning import commit_all
from .services.reports import totals_by_partner
from .utils.paths import ROOT, CONTRACTS_DIR

app = typer.Typer(add_completion=False, help="Contractor CLI")

@app.command("init-db")
def init_db_cmd():
    init_db()
    print("[green]Database initialized.[/green]")

@app.command("party-add")
def party_add(name: str, country: str = typer.Option(None)):
    with get_session() as s:
        p = Party(name=name, country=country)
        s.add(p)
        s.commit()
        s.refresh(p)
        print(f"[cyan]Party created with id={p.id}[/cyan]")

@app.command("template-list")
def template_list():
    for t in available_templates():
        print("-", t)

@app.command("contract-new")
def contract_new(
    template: str = typer.Option("basic_zh", "--template"),
    data: Path = typer.Option(..., "--data", exists=True, file_okay=True),
    version: str = "0.1.0",
    outdir: Path = typer.Option(Path("contracts"), "--outdir", file_okay=False),
):
    ctx = yaml.safe_load(data.read_text(encoding="utf-8"))
    party_name = ctx.get("party", {}).get("name", "Unknown")
    with get_session() as s:
        party = s.exec(select(Party).where(Party.name == party_name)).first()
        if not party:
            party = Party(name=party_name, country=ctx.get("party", {}).get("country"))
            s.add(party); s.commit(); s.refresh(party)
        amount_minor = int(round(float(ctx.get("amount", {}).get("value", 0.0)) * 100))
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
        doc_id = f"contract_{c.id}_v{c.version}"
        outdir = outdir / str(c.id)
        tex_path = render_tex(f"contract_{template}.tex.j2", ctx | {"document_id": doc_id}, outdir)
        s.add(ContractFile(contract_id=c.id, kind="tex", path=str(tex_path))); s.commit()
        print(f"[green]Contract {c.id} created and .tex rendered at {tex_path}[/green]")

@app.command("contract-render")
def contract_render(
    id: int = typer.Option(..., "--id"),
    pdf: bool = typer.Option(False, "--pdf"),
    docx: bool = typer.Option(False, "--docx"),
):
    engine = os.getenv("LATEX_ENGINE", "tectonic")
    with get_session() as s:
        c = s.get(Contract, id)
        if not c:
            print("[red]Contract not found[/red]"); raise typer.Exit(1)
        outdir = Path("contracts") / str(c.id)
        tex_path = outdir / f"contract_{c.id}_v{c.version}.tex"
        if not tex_path.exists():
            print("[yellow].tex not found. Nothing to render.[/yellow]"); raise typer.Exit(1)
        if pdf:
            pdf_path = compile_pdf(tex_path, engine=engine)
            if pdf_path:
                s.add(ContractFile(contract_id=id, kind="pdf", path=str(pdf_path))); s.commit()
                print(f"[green]PDF created: {pdf_path}[/green]")
        if docx:
            docx_path = tex_to_docx(tex_path)
            if docx_path:
                s.add(ContractFile(contract_id=id, kind="docx", path=str(docx_path))); s.commit()
                print(f"[green]DOCX created: {docx_path}[/green]")

@app.command("report-totals")
def report_totals(currency: str = "CNY"):
    totals = totals_by_partner(currency=currency)
    print(json.dumps(totals, ensure_ascii=False, indent=2))

@app.command("repo-commit")
def repo_commit(message: str = typer.Option("Update artifacts")):
    ok = commit_all(Path.cwd(), message)
    print("[green]Committed.[/green]" if ok else "[yellow]Nothing to commit or git failed.[/yellow]")

if __name__ == "__main__":
    app()
