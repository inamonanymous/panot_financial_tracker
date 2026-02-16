"""Helper to create GitHub issues from `TRACKING/issues/*.md` using `gh` CLI.

Usage:
  - Dry run (no remote changes):
      python scripts/create_github_issues_from_md.py
  - To actually create issues (requires `gh` authenticated):
      python scripts/create_github_issues_from_md.py --apply

The script prefers `gh` CLI; it prints the `gh` commands it would run.
"""
import argparse
import shlex
import subprocess
from pathlib import Path

ISSUES_DIR = Path(__file__).resolve().parents[1] / 'TRACKING' / 'issues'


def parse_title_from_md(path: Path):
    text = path.read_text(encoding='utf-8')
    # First non-empty line treated as title when starts with 'Title:'
    for line in text.splitlines():
        if line.strip().startswith('Title:'):
            return line.partition(':')[2].strip()
    # fallback to filename
    return path.stem


def main(apply: bool):
    gh = shutil_which('gh')
    if gh is None and apply:
        print('ERROR: `gh` CLI not found. Install GitHub CLI or run in dry-run mode.')
        return

    files = sorted(ISSUES_DIR.glob('*.md'))
    if not files:
        print('No issue markdown files found in', ISSUES_DIR)
        return

    for f in files:
        title = parse_title_from_md(f)
        cmd = f"gh issue create --title {shlex.quote(title)} --body-file {shlex.quote(str(f))} --label use-case,backend"
        print('DRY-RUN CMD: ', cmd)
        if apply:
            print('Running:', cmd)
            subprocess.run(cmd, shell=True)


def shutil_which(name: str):
    from shutil import which
    return which(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Actually create issues using gh')
    args = parser.parse_args()
    main(args.apply)
