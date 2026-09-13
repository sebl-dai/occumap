"""Lexical SSOC candidate retrieval. Pure: no disk, no network."""

from dataclasses import dataclass

import pandas as pd

STOPWORDS = {
    "and", "or", "the", "of", "in", "at", "to", "for",
    "a", "an", "senior", "junior", "assistant", "associate",
    "chief", "head", "lead", "principal", "deputy", "asst",
    "snr", "sr", "jnr", "jr", "pt", "part", "time",
}


@dataclass(frozen=True)
class Candidate:
    """One ranked SSOC code for a title."""

    ssoc_code: str
    title: str
    split: str
    score: float


def _score_row(row: pd.Series, title_clean: str, content_words: set[str]) -> int:
    """Score one SSOC row against a cleaned title. Same five terms as notebook cell 6."""
    ssoc_title = str(row["title"]).lower()
    ssoc_words = set(ssoc_title.split()) - STOPWORDS
    examples = str(row.get("examples_here", "")).lower()
    definition = str(row.get("definition", "")).lower()

    phrase_match = 10 if title_clean in ssoc_title else 0
    example_phrase = 8 if title_clean in examples else 0
    word_overlap = len(content_words & ssoc_words) * 2
    example_word = sum(2 for word in content_words if word in examples)
    definition_word = sum(1 for word in content_words if word in definition)

    return phrase_match + example_phrase + word_overlap + example_word + definition_word


def retrieve(title: str | None, ssoc: pd.DataFrame, k: int) -> list[Candidate]:
    """Rank SSOC rows against a title by word match and return the top k.

    Only rows scoring above 0 are kept, highest score first. Returns an empty
    list for an empty title, a title of only stopwords, or no matching rows.
    `ssoc` is the frame from loaders.load_ssoc.
    """
    if not title or str(title).strip() == "":
        return []

    title_clean = str(title).lower().strip()
    content_words = set(title_clean.split()) - STOPWORDS
    if not content_words:
        return []

    scored = ssoc.copy()
    scored["score"] = scored.apply(
        lambda row: _score_row(row, title_clean, content_words), axis=1
    )
    top = scored[scored["score"] > 0].nlargest(k, "score")

    return [
        Candidate(
            ssoc_code=row["ssoc_code"],
            title=row["title"],
            split=row["split"],
            score=float(row["score"]),
        )
        for _, row in top.iterrows()
    ]


def format_candidates(candidates: list[Candidate]) -> str:
    """Build the candidate block for the classification prompt.

    Returns an empty string for no candidates, so the prompt gets no header.
    """
    if not candidates:
        return ""

    lines = ["Candidate SSOC codes (choose from these if relevant):"]
    for candidate in candidates:
        lines.append(f"- {candidate.ssoc_code}: {candidate.title} ({candidate.split})")

    return "\n".join(lines)
