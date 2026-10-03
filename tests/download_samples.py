"""Download a reproducible sample of public resume PDFs for evaluation.

Source: https://huggingface.co/datasets/d4rk3r/resumes-raw-pdf (MIT licensed). The PDFs are
real-world resumes, so they are saved to tests/data/ which is git-ignored. Do not commit them.

    python tests/download_samples.py --n 100 --seed 7 --out tests/data/holdout
"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import urllib.request

API = "https://huggingface.co/api/datasets/d4rk3r/resumes-raw-pdf/tree/main/{}"
RAW = "https://huggingface.co/datasets/d4rk3r/resumes-raw-pdf/resolve/main/{}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", default="it-domain", help="dataset folder: it-domain or all-domains")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default="tests/data/holdout")
    a = ap.parse_args()

    items = [i for i in json.load(urllib.request.urlopen(API.format(a.folder), timeout=60))
             if i["path"].endswith(".pdf")]
    random.seed(a.seed)
    pick = random.sample(items, a.n)
    os.makedirs(a.out, exist_ok=True)

    def get(i):
        urllib.request.urlretrieve(RAW.format(i["path"]), os.path.join(a.out, os.path.basename(i["path"])))

    with cf.ThreadPoolExecutor(8) as ex:
        list(ex.map(get, pick))
    print(f"{len(pick)} PDFs saved to {a.out}")


if __name__ == "__main__":
    main()
