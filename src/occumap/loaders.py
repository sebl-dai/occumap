"""Data loading. Everything that touches disk lives here."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_titles(path: Path | None = None) -> pd.DataFrame:
    """Load the synthetic occupation titles."""
    path = path or DATA_DIR / "synthetic_titles.csv"
    return pd.read_csv(path)


def _split_from_major_group(major_group: str) -> str:
    """Map an SSOC major group digit to its workforce split."""
    if major_group in ("1", "2"):
        return "PME"
    if major_group == "3":
        return "T"
    if major_group in ("4", "5", "6", "7", "8", "9"):
        return "RNF"
    return "NA"


def load_ssoc(path: Path | None = None) -> pd.DataFrame:
    """Load SSOC 2024 definitions, filtered to 5-digit occupation codes."""
    path = path or DATA_DIR / "ssoc2024-detailed-definitions.xlsx"

    ssoc = pd.read_excel(
        path,
        sheet_name="SSOC2024 Detailed Definitions",
        header=4,
    )

    ssoc.columns = [
        "ssoc_code",
        "title",
        "groups",
        "definition",
        "tasks",
        "notes",
        "examples_here",
        "examples_elsewhere",
    ]

    ssoc = ssoc[ssoc["ssoc_code"].notna()].copy()
    ssoc["ssoc_code"] = ssoc["ssoc_code"].astype(str).str.strip()
    ssoc["major_group"] = ssoc["ssoc_code"].str[0]
    ssoc["split"] = ssoc["major_group"].apply(_split_from_major_group)

    return ssoc[ssoc["ssoc_code"].str.len() == 5].copy()
