"""Build the collagen benchmark page in each language.

Fills src/template.html with the strings in src/i18n/<lang>.json and writes
collagen-comparison.html (English) and collagen-comparison.<lang>.html.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
LANGS = ["en", "ru", "uz"]
PLACEHOLDER = re.compile(r"\{\{([\w.]+)\}\}")


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def build(lang):
    template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    data = json.loads((ROOT / "src" / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
    if data["units"]["thou"] == " ":
        data["units"]["thou"] = " "  # keep digit groups on one line
    strings = flatten({k: v for k, v in data.items() if k not in ("units", "js", "products")})
    runtime = {"units": data["units"], "js": data["js"], "products": data["products"]}
    strings["__T"] = json.dumps(runtime, ensure_ascii=False).replace("</", "<\\/")

    missing = sorted({m for m in PLACEHOLDER.findall(template) if m not in strings})
    if missing:
        raise SystemExit(f"{lang}: missing strings {missing}")
    html = PLACEHOLDER.sub(lambda m: str(strings[m.group(1)]), template)

    name = "collagen-comparison.html" if lang == "en" else f"collagen-comparison.{lang}.html"
    (ROOT / name).write_text(html, encoding="utf-8")
    print("wrote", name)


if __name__ == "__main__":
    for lang in LANGS:
        build(lang)
