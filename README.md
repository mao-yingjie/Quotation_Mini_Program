
# Contractor — Python Contract Automation (LaTeX → PDF & Word)

Authoring in **LaTeX (with Jinja2)**, producing **PDF** via Tectonic/XeLaTeX and **Word (.docx)** via **Pandoc**.

## Quick Start (openSUSE)
```bash
sudo zypper install tectonic
sudo zypper install pandoc
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
contractor init-db
contractor contract new --template basic_zh --data data/sample_contract.yml --outdir contracts
contractor contract render --id 1 --pdf --docx
```
