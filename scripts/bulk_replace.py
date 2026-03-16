#!/usr/bin/env python3
"""
bulk_replace.py - simple interactive bulk text replacer

Usage:
  python scripts/bulk_replace.py --dir G2_Site_Template28

The script contains a small set of default replacements (the ones we used
in the G2_Site_Template28 work). It will scan files under the given
directory, report matches, and ask for confirmation before applying each
replacement. You can also add new replacements interactively while the
script is running.

Notes:
- The script works on text files only (it skips files that can't be decoded
  as UTF-8).
- Before overwriting a file it creates a .bak copy next to the file.
- Replacements are literal substring replacements (not regular expressions).
"""

from pathlib import Path
import argparse
import shutil
import sys


DEFAULT_REPLACEMENTS = [
    # addresses
    {
        "find": "9250 NW 25TH STREET\nDORAL, FL 33172",
        "replace": "6320 PEMBROKE ROAD\nMIRAMAR, FL 33023",
    },
    {
        "find": "4978 Millenia Blvd # C, Orlando, FL 32839",
        "replace": "6320 PEMBROKE ROAD\nMIRAMAR, FL 33023",
    },
    # favicon inline SVG data -> remote favicon
    {
        "find": (
            "<link rel=\"icon\"\n        href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
            "viewBox='0 0 24 24' fill='none' stroke='%232563EB' stroke-width='2' "
            "stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 21h18M5 21V7l8-4 8 4v14'/%3E%3C/svg%3E\" />"
        ),
        "replace": '<link rel="icon" href="https://nextgeeninvesting.com/wp-content/uploads/2025/03/cropped-nextgeen-32x32.png" sizes="32x32" />',
    },
]


def iter_text_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file():
            # try to read a chunk as UTF-8 to skip binaries
            try:
                with p.open("rb") as fh:
                    sample = fh.read(4096)
                sample.decode("utf-8")
            except Exception:
                # skip binary / non-UTF-8 files
                continue
            yield p


def find_matches(root: Path, find: str):
    matches = {}
    for p in iter_text_files(root):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        cnt = text.count(find)
        if cnt:
            matches[p] = cnt
    return matches


def apply_replacement(root: Path, find: str, replace: str):
    total_files = 0
    total_replacements = 0
    for p in iter_text_files(root):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if find in text:
            new_text = text.replace(find, replace)
            # backup
            bak = p.with_suffix(p.suffix + ".bak")
            shutil.copy2(p, bak)
            p.write_text(new_text, encoding="utf-8")
            num = text.count(find)
            total_files += 1
            total_replacements += num
            print(f"Updated {p} — {num} replacements (backup: {bak.name})")
    return total_files, total_replacements


def interactive_loop(root: Path, replacements):
    for pair in replacements:
        find = pair["find"]
        replace = pair["replace"]
        print("\n=== Replacement Preview ===")
        print("Find:\n", find)
        print("Replace:\n", replace)
        matches = find_matches(root, find)
        if not matches:
            print("No matches found under", root)
            cont = input("Apply anyway? (y/N): ").strip().lower()
            if cont != "y":
                continue
        else:
            total = sum(matches.values())
            print(f"Found {total} matches in {len(matches)} files. Sample:")
            for i, (p, c) in enumerate(matches.items()):
                print(f" - {p} : {c}")
                if i >= 4:
                    break
            do = input("Apply replacement now? (y/N): ").strip().lower()
            if do != "y":
                continue
        files, repls = apply_replacement(root, find, replace)
        print(f"Done — updated {files} files with {repls} total replacements.")

    # allow adding new replacements
    while True:
        more = input("Add another replacement? (y/N): ").strip().lower()
        if more != "y":
            break
        print("Enter the exact text to FIND (use \n for new lines). Finish input with an empty line:")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        find = "\n".join(lines)
        print("Enter the replacement text (use \n for new lines). Finish with an empty line:")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        replace = "\n".join(lines)
        interactive_loop(root, [{"find": find, "replace": replace}])


def main():
    ap = argparse.ArgumentParser(description="Bulk text replacement tool (interactive)")
    ap.add_argument("--dir", "-d", default="G2_Site_Template28", help="Target directory to scan/replace")
    ap.add_argument("--no-defaults", action="store_true", help="Do not run the bundled default replacements")
    args = ap.parse_args()

    root = Path(args.dir)
    if not root.exists() or not root.is_dir():
        print("Target directory does not exist:", root)
        sys.exit(1)

    replacements = []
    if not args.no_defaults:
        replacements.extend(DEFAULT_REPLACEMENTS)

    if replacements:
        interactive_loop(root, replacements)

    # enter interactive add-loop even if no defaults
    print("Finished. You can run the script again or add new replacements interactively next time.")


if __name__ == "__main__":
    main()
