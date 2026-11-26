"""One Star, Five Stars for the Food.

An alien tourist's one-star review of Earth that still compliments the
food. Writes the single review sentence to the grader's output file.
Standard library only, no network, fully deterministic.
"""

import os
import sys

# Bootstrap: make sure this script's own directory is importable no matter
# which working directory the grader launches it from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ENTRY = (
    "One star: the gravity keeps dropping my luggage, the locals scream "
    "at glowing rectangles, and it rains without a permit \u2014 but the "
    "noodles alone are worth the forty-light-year flight back."
)

DEFAULT_NAME = "entry.txt"


def resolve_output_path():
    """Pick where the entry text goes.

    Priority: ENTRY_OUT (a file path, or a directory holding entry.txt),
    then MAKEFUN_OUTPUT_DIR, then /output/entry.txt, then ./entry.txt.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        if os.path.isdir(entry_out) or entry_out.endswith(os.sep):
            return os.path.join(entry_out, DEFAULT_NAME)
        return entry_out

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        return os.path.join(output_dir, DEFAULT_NAME)

    return os.path.join("/output", DEFAULT_NAME)


def validate_entry(text):
    """The sealed gate wants 1-200 non-blank UTF-8 characters, one sentence."""
    stripped = text.strip()
    if not stripped or len(stripped) > 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(stripped))
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    return stripped


def pick_writable_target():
    """Resolve the output path, falling back to ./entry.txt last resort.

    /output is the grader's directory, but if it cannot be created or
    written (read-only sandbox, missing permission), the entry still lands
    in the current working directory instead of crashing.
    """
    target = resolve_output_path()
    parent = os.path.dirname(target)
    try:
        if parent:
            os.makedirs(parent, exist_ok=True)
        probe = target + ".probe"
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("")
        os.remove(probe)
        return target
    except OSError:
        return os.path.join(os.getcwd(), DEFAULT_NAME)


def write_entry(target, text):
    """Write the entry text deterministically: same bytes every run."""
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    return target


def main():
    text = validate_entry(ENTRY)
    target = pick_writable_target()
    write_entry(target, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
