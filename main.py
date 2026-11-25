"""One Line, One Chill - stdlib-only copier.

Reads entry.txt next to this file and writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt, validating the result.
"""

import hashlib
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")

    with open(src, "r", encoding="utf-8") as f:
        line = f.read()

    line = line.strip()
    if not line:
        print("entry.txt is empty", file=sys.stderr)
        return 1
    if len(line) >= 200:
        print("line is %d chars, must be under 200" % len(line), file=sys.stderr)
        return 1
    if "\n" in line:
        print("line must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(line + "\n")

    with open(out_path, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    # Verify the written output round-trips exactly to the source line.
    if data.decode("utf-8").strip() != line:
        print("output does not match source line", file=sys.stderr)
        return 1
    if not line.endswith((".", "!", "?")):
        print("line must end with sentence punctuation", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
