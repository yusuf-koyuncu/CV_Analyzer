"""Evaluate parser.py on a folder of PDF resumes.

Ground truth comes from an independent extractor (poppler's `pdftotext`, which must be on PATH)
plus strict name/alias regexes, so it measures how well parser.py finds the 15 listed skills in
the text, not whether a candidate really has them. PDFs with no extractable text (scans) are
reported separately and contribute no skills.

    python tests/evaluate.py tests/data/holdout
"""
import collections
import glob
import os
import re
import statistics
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import parser as P  # noqa: E402

TRUTH = {
    "Python": r"\bpython\d*\b", "SQL": r"\bsql\b", "React": r"\breact(?:\.?js)?\b",
    "JavaScript": r"\bjavascript\b|(?<![\w.])js\b", "C#": r"c\s?#|c-sharp|csharp",
    "C++": r"c\s?\+\s?\+|\bcpp\b", "Java": r"\bjava\b", "Docker": r"\bdocker\b", "Git": r"\bgit\b",
    "HTML": r"\bhtml\d*\b", "CSS": r"\bcss\d*\b", "Node.js": r"\bnode\.?\s?js\b|\bnodejs\b",
    "Django": r"\bdjango\b", "PostgreSQL": r"\bpostgres(?:ql)?\b", "AWS": r"\baws\b|amazon web services",
}


def reference_text(path):
    return subprocess.run(["pdftotext", "-q", path, "-"], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "tests/data/holdout"
    files = sorted(glob.glob(os.path.join(folder, "*.pdf")))
    if not files:
        sys.exit(f"No PDFs in {folder}")

    tp = fp = fn = scanned = 0
    ms, errors = [], []
    for f in files:
        ref = reference_text(f)
        scanned += not ref.strip()
        truth = {k for k, rx in TRUTH.items() if re.search(rx, ref, re.I)}
        t0 = time.perf_counter()
        text = P.extract_text_from_pdf(f)
        found = set() if text.startswith("Hata") else set(P.find_skills(text))
        ms.append((time.perf_counter() - t0) * 1000)
        tp += len(truth & found)
        fp += len(found - truth)
        fn += len(truth - found)
        errors += [("FP", os.path.basename(f), k) for k in found - truth]
        errors += [("FN", os.path.basename(f), k) for k in truth - found]

    ms.sort()
    print(f"{len(files)} PDFs ({scanned} without extractable text)")
    print(f"TP={tp} FP={fp} FN={fn}  precision={tp / (tp + fp):.3f}  recall={tp / (tp + fn):.3f}")
    print(f"time per CV: mean {statistics.mean(ms):.0f} ms, median {statistics.median(ms):.0f} ms, "
          f"p95 {ms[int(0.95 * len(ms)) - 1]:.0f} ms, max {ms[-1]:.0f} ms")
    for kind, name, skill in errors:
        print(f"  {kind} {name}: {skill}")
    print("misses by skill:", collections.Counter(s for k, _, s in errors if k == "FN").most_common())


if __name__ == "__main__":
    main()
