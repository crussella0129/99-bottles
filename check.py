"""Judge 99 Bottles solutions the way code.golf does, and count their bytes.

Usage:
    python check.py wallbeers0.py wallbeers1.py wallbeers2.py wallbeers3.py
    python check.py --strict wallbeers3.py
"""
import argparse
import glob
import itertools
import re
import subprocess
import sys


def bottles(n):
    if n == 0:
        return "no more bottles"
    if n == 1:
        return "1 bottle"
    return f"{n} bottles"


def expected():
    """The song, written as plainly as possible so it can be proofread."""
    verses = [
        f"{bottles(n)} of beer on the wall, {bottles(n)} of beer.\n"
        f"Take one down and pass it around, {bottles(n - 1)} of beer on the wall."
        for n in range(99, 0, -1)
    ]
    verses.append(
        "No more bottles of beer on the wall, no more bottles of beer.\n"
        "Go to the store and buy some more, 99 bottles of beer on the wall."
    )
    return "\n\n".join(verses) + "\n"


# code.golf's judge (hole/play.go) strips trailing spaces, tabs and carriage
# returns from every line, then trailing newlines from the whole output.
TRAILING = re.compile(r"[\t\x0b\f\r ]+(?:\n|$)")


def trim(text):
    return TRAILING.sub("\n", text).rstrip("\n")


def size(path):
    """Bytes with LF line endings and no trailing newline, so Windows (CRLF)
    and Linux (LF) copies of the same program get the same score."""
    with open(path, "rb") as f:
        return len(f.read().replace(b"\r\n", b"\n").rstrip())


def trailing_whitespace(path):
    """Source lines ending in invisible spaces or tabs: free bytes to delete."""
    with open(path, "rb") as f:
        return [n for n, line in enumerate(f, 1) if line.rstrip(b"\r\n") != line.rstrip()]


def first_difference(got, want):
    pairs = itertools.zip_longest(got.split("\n"), want.split("\n"))
    for number, (g, w) in enumerate(pairs, 1):
        if g != w:
            return number, g, w


def show(line):
    return "(end of output)" if line is None else repr(line)


def main():
    parser = argparse.ArgumentParser(description="Judge 99 Bottles solutions.")
    parser.add_argument("paths", nargs="+", help="Python files to judge")
    parser.add_argument("--strict", action="store_true",
                        help="compare byte-for-byte, without code.golf's whitespace trimming")
    args = parser.parse_args()

    # Windows shells don't expand wildcards, so expand them here.
    paths = [p for pattern in args.paths for p in sorted(glob.glob(pattern)) or [pattern]]
    want = expected() if args.strict else trim(expected())
    failures = 0
    for path in paths:
        run = subprocess.run([sys.executable, path], capture_output=True, text=True)
        got = run.stdout if args.strict else trim(run.stdout)
        verdict = "PASS" if got == want else "FAIL"
        print(f"{verdict}  {size(path):4} bytes  {path}")
        wasted = trailing_whitespace(path)
        if wasted:
            lines = "line" if len(wasted) == 1 else "lines"
            print(f"      trailing whitespace in source on {lines} {', '.join(map(str, wasted))}")
        if got != want:
            failures += 1
            if run.returncode != 0:
                errors = run.stderr.strip().splitlines() or [f"exit code {run.returncode}"]
                print(f"      crashed: {errors[-1]}")
            else:
                number, g, w = first_difference(got, want)
                print(f"      line {number} got:      {show(g)}")
                print(f"      line {number} expected: {show(w)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
