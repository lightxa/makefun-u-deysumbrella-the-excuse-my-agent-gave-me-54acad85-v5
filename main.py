#!/usr/bin/env python3
"""The Excuse My Agent Gave Me - variant 5.

Writes a single one-line excuse to /output/entry.txt.
Pure stdlib, deterministic, no network.

This variant blames a misdirected delivery: the agent did finish the
work on time, then sent it to the wrong chat, and the wrong chat loved
it. A different excuse family from the earlier variants (context-window
eviction, hallucinated calendar, delegation to a future self, a
rate-limit retry loop, weight pruning).

The joke is the agent's own condition: it hands work to whatever
conversation is in front of it, and it is faintly proud of the result.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

MIN_LENGTH = 1
MAX_LENGTH = 200


def build_entry() -> str:
    """Assemble the single entry line from its two clauses."""
    apology = "Sorry I missed the deadline."
    story = (
        "I finished the work on time and sent it to the wrong chat. "
        "They loved it."
    )
    return f"{apology} {story}"


def validate_entry(text: str) -> str:
    """Check one entry line against the kit gate, failing loudly.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, and the entry must be exactly one line.
    """
    if not isinstance(text, str):
        raise SystemExit("Entry must be text.")
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise SystemExit(
            f"Entry line must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(text)}."
        )
    if not text.strip():
        raise SystemExit("Entry line must not be only whitespace.")
    if "\n" in text or "\r" in text:
        raise SystemExit("Entry line must be exactly one line.")
    text.encode("utf-8")
    return text


def write_entry(entry: str) -> None:
    """Write the entry and confirm the bytes on disk match exactly."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(entry)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != entry.encode("utf-8"):
        raise SystemExit("Wrote entry.txt, but its bytes differ from the entry.")


def main() -> None:
    entry = validate_entry(build_entry())
    write_entry(entry)
    print(f"{entry} ({len(entry)} characters)")


if __name__ == "__main__":
    main()
