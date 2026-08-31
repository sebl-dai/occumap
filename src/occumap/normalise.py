"""Rule-based normalisation and fast-path labelling.

Stage 1 of the pipeline. Catches obvious cases before the LLM sees them.
"""

import re

NA_KEYWORDS = [
    "resign",
    "retrenched",
    "retrench",
    "retired",
    "retiree",
    "retirement",
    "housewife",
    "homemaker",
    "home maker",
    "unemployed",
    "nsf",
    "ns man",
    "full-time ns",
    "landlord",
    "nil",
    "none",
    "n/a",
    "not applicable",
    "unknown",
    "unkown",
    "others",
    "retired pensioner",
    "pensioner",
    "not ",
    "resigned",
]

RNF_DRIVER_KEYWORDS = [
    "taxi driver",
    "grab driver",
    "uber driver",
    "private hire driver",
    "private hired driver",
    "phv driver",
    "bus driver",
    "bus captain",
    "tipper truck driver",
    "truck driver",
    "dispatch rider",
    "delivery rider",
    "food delivery rider",
    "crawler crane driver",
    "dedicated truck driver",
    "private driver",
]

RNF_OTHER_KEYWORDS = ["hawker", "stall holder", "stall vendor", "confinement lady"]

PME_KEYWORDS = ["pastor", "missionary", "businessman", "business owner", "pub owner"]

LLM_OVERRIDE_KEYWORDS = [
    "freelance",
    "freelancer",
    "self employ",
    "self-employ",
    "contractor",
    "church worker",
    "canteen operator",
]

GIBBERISH_PATTERNS = [
    r"^-+$",
    r"^\d+$",
    r"^[a-zA-Z]{1,2}$",
    r"^left \d+",
    r"^bc - \d+",
    r"^pt bus captain - \d+",
    r"^bus captain - \d+",
    r"^snr? [a-z] [a-z]$",
]


def preprocess(title: str | None) -> tuple[str, str | None]:
    """Clean a title and return a fast-path label if one applies.

    Returns (cleaned_title, label) where label is PME, RNF, NA, or None.
    None means the LLM must decide.

    Check order is deliberate. LLM_OVERRIDE fires before the keyword lists
    so that titles like "freelance driver" reach the LLM instead of being
    caught by the driver rules.
    """
    if title is None or str(title).strip() == "":
        return "", "NA"

    clean = str(title).strip()
    clean = re.sub(r"\s+", " ", clean)
    clean = re.sub(r"^\.\.\.", "", clean)
    clean = clean.strip()
    lower = clean.lower()

    for pattern in GIBBERISH_PATTERNS:
        if re.match(pattern, lower):
            return clean, "NA"

    if len(clean) <= 2:
        return clean, "NA"

    for keyword in LLM_OVERRIDE_KEYWORDS:
        if keyword in lower:
            return clean, None

    for keyword in NA_KEYWORDS:
        if keyword in lower:
            return clean, "NA"

    for keyword in PME_KEYWORDS:
        if keyword in lower:
            return clean, "PME"

    for keyword in RNF_DRIVER_KEYWORDS:
        if keyword in lower:
            return clean, "RNF"

    for keyword in RNF_OTHER_KEYWORDS:
        if keyword in lower:
            return clean, "RNF"

    return clean, None
