
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = ROOT / "templates" / "latex"
PANDOC_DIR = ROOT / "templates" / "pandoc"
CONTRACTS_DIR = ROOT / "contracts"
DATA_DIR = ROOT / "data"
DB_DEFAULT = ROOT / "contractor.db"
