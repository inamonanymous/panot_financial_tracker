"""Generate basic trackers from code (use-cases -> routes -> components).

Usage: python scripts/generate_trackers.py

This script scans `app/use_cases` and `app/routes` and writes `TRACKING/trackers.json` and `TRACKING/USE_CASES.md`.
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USE_CASES_DIR = ROOT / "app" / "use_cases"
ROUTES_DIR = ROOT / "app" / "routes"
TRACKING_DIR = ROOT / "TRACKING"
TRACKING_JSON = TRACKING_DIR / "trackers.json"
TRACKING_MD = TRACKING_DIR / "USE_CASES.md"


def find_routes_for_class(class_name: str):
    matches = []
    for f in ROUTES_DIR.glob('*.py'):
        text = f.read_text(encoding='utf-8')
        if class_name in text:
            # try to capture route names or function names for context
            # fallback to filename
            m = re.search(r"@\w+\.route\('([^']+)'", text)
            route_snippets = re.findall(r"@\w+\.route\('([^']+)'", text)
            snippet = ','.join(route_snippets) if route_snippets else ''
            matches.append(f"{f.name}{(':' + snippet) if snippet else ''}")
    return matches


def extract_usecases_from_file(path: Path):
    content = path.read_text(encoding='utf-8')
    module = ast.parse(content)
    module_doc = ast.get_docstring(module) or ''
    results = []
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name.endswith('UseCase'):
            cls_doc = ast.get_docstring(node) or module_doc or ''
            results.append({'class': node.name, 'doc': cls_doc.strip()})
    # If no class found but module docstring exists, try to infer one use-case from filename
    if not results and module_doc:
        # infer by filename
        derived = path.stem
        results.append({'class': derived, 'doc': module_doc.strip()})
    return results


def main():
    out = []
    idx = 1
    for py in USE_CASES_DIR.rglob('*.py'):
        entries = extract_usecases_from_file(py)
        for e in entries:
            cname = e['class']
            routes = find_routes_for_class(cname)
            # heuristic: look for policy or model imports inside file
            txt = py.read_text(encoding='utf-8')
            policies = re.findall(r"from app\.domain\.policies\.(p_[A-Za-z0-9_]+)", txt)
            models = re.findall(r"from app\.model\.([A-Za-z0-9_]+)", txt)
            components = policies + models
            out.append({
                'id': f'UC-{idx:03d}',
                'name': cname,
                'file': str(py.relative_to(ROOT)),
                'routes': routes,
                'description': e['doc'][:200],
                'status': 'Backlog',
                'components': components,
            })
            idx += 1

    TRACKING_DIR.mkdir(parents=True, exist_ok=True)
    TRACKING_JSON.write_text(json.dumps({'use_cases': out}, indent=2), encoding='utf-8')

    # render a small markdown table
    md_lines = [
        '# Use Case Tracker (auto-generated)\n',
        '| ID | Use case | File | Route(s) | Short description | Status | Components |',
        '|---:|---|---|---|---|---|---|',
    ]
    for u in out:
        routes = ', '.join(u['routes']) if u['routes'] else ''
        comps = ', '.join(u['components']) if u['components'] else ''
        md_lines.append(f"| {u['id']} | {u['name']} | `{u['file']}` | {routes} | {u['description']} | {u['status']} | {comps} |")

    TRACKING_MD.write_text('\n'.join(md_lines), encoding='utf-8')

    print(f"Wrote {TRACKING_JSON} ({len(out)} use-cases) and updated {TRACKING_MD}")


if __name__ == '__main__':
    main()
