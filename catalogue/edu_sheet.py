"""Round-trip the guide copy through a spreadsheet so translators can correct it.

    python3 catalogue/edu_sheet.py export   # writes out/yorosum-guide-text.csv (opens in Excel / Google Sheets)
    python3 catalogue/edu_sheet.py import <file.csv>   # writes the Russian and Uzbek columns back into edu_i18n.json

Then run python3 catalogue/edu.py to rebuild the PDFs.
"""
import csv
import json
import sys

from build import OUT, ROOT

SRC = ROOT / "edu_i18n.json"
SKIP = {"html_lang", "flag", "u_mg", "u_da", "n2000", "c_title", "c_sub"}
PAGE = {"c": 1, "p2": 2, "p3": 3, "p4": 4, "p5": 5, "ing": 5, "inc": 5, "m1": 5, "m2": 5, "m3": 5, "pick": 0, "lang": 0}


def page_of(key):
    return PAGE.get(key.split("_")[0], PAGE.get(key.rstrip("0123456789_v"), ""))


def export():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    path = OUT / "yorosum-guide-text.csv"
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "page", "English (reference)", "Russian", "Uzbek"])
        for k in d["en"]:
            if k not in SKIP:
                w.writerow([k, page_of(k), d["en"][k], d["ru"].get(k, ""), d["uz"].get(k, "")])
    print(path)


def import_(path):
    d = json.loads(SRC.read_text(encoding="utf-8"))
    changed = 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            k = row["key"]
            for lang, col in (("ru", "Russian"), ("uz", "Uzbek")):
                v = (row.get(col) or "").strip()
                if k in d[lang] and v and v != d[lang][k]:
                    print(f"{lang} {k}: {d[lang][k]!r} -> {v!r}")
                    d[lang][k] = v
                    changed += 1
    SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(changed, "changes")


if __name__ == "__main__":
    export() if sys.argv[1] == "export" else import_(sys.argv[2])
