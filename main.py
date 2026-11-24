"""Entrypoint for news-image-20261123 (account 2).

The grader runs Python 3.13 with only the standard library, so this file
copies the pre-built entry.png next to it into $MAKEFUN_OUTPUT_DIR.
It never imports Pillow and never touches the network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    if os.path.getsize(src) > 1024 * 1024:
        print("entry.png exceeds the 1 MiB cap", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
