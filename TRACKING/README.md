# Project Trackers

This folder contains lightweight trackers for features, use-cases, and component dependencies — plus a small generator script to keep them in sync with the codebase.

Quick commands:
- Regenerate use-case tracker: `python scripts/generate_trackers.py`
- Format / edit trackers directly in `TRACKING/*.md`

Files included:
- `USE_CASES.md` — one-row-per-use-case with routes, components and status
- `FEATURES.md` — high-level features mapped to use-cases
- `COMPONENT_DEPENDENCIES.md` — cross-layer prerequisites and relationships
- `DEPENDENCY_GRAPH.mmd` — mermaid diagram skeleton for quick visualization
- `trackers.json` — machine-readable snapshot

Why this helps
- Keeps technical ownership and prerequisites visible at the code level
- Makes it easy to move items between Backlog / In Progress / Done
- Generator script allows quick refresh when new use-cases are added

— end of tracker README —