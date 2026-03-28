from __future__ import annotations

import gzip
import json
import shutil
import time
from pathlib import Path
from urllib.request import urlopen, Request

# =========================
# НАСТРОЙКИ
# =========================
BASE_URL = "https://storage.googleapis.com/gresearch/dialog-inpainting/WikiDialog_OQ"

DOWNLOAD_DIR = Path("datasets/wiki_dialog_oq_download").resolve()
OUTPUT_DIR = Path("datasets/wiki_dialog_oq_jsonl").resolve()

TRAIN_OUT = OUTPUT_DIR / "wiki_dialog_oq_train.jsonl"
VALID_OUT = OUTPUT_DIR / "wiki_dialog_oq_validation.jsonl"

TRAIN_SHARDS = 99
TIMEOUT = 120
USER_AGENT = "Mozilla/5.0"


def ensure_dirs() -> None:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, chunk_size: int = 1024 * 1024) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] already exists: {dest.name}")
        return

    print(f"[download] {url}")
    req = Request(url, headers={"User-Agent": USER_AGENT})

    with urlopen(req, timeout=TIMEOUT) as response, dest.open("wb") as f:
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)

    print(f"[saved] {dest}")


def append_gzip_jsonl_to_jsonl(gz_path: Path, out_path: Path) -> int:
    count = 0
    with gzip.open(gz_path, "rt", encoding="utf-8") as fin, out_path.open("a", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            # Проверка, что строка — валидный JSON.
            obj = json.loads(line)

            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")
            count += 1

    return count


def build_train_urls() -> list[tuple[str, Path]]:
    items = []
    for i in range(TRAIN_SHARDS):
        filename = f"data_train.jsonl-{i:05d}-of-00099.gz"
        url = f"{BASE_URL}/{filename}"
        dest = DOWNLOAD_DIR / filename
        items.append((url, dest))
    return items


def build_validation_url() -> tuple[str, Path]:
    filename = "data_validation.jsonl.gz"
    url = f"{BASE_URL}/{filename}"
    dest = DOWNLOAD_DIR / filename
    return url, dest


def main() -> None:
    ensure_dirs()

    if TRAIN_OUT.exists():
        TRAIN_OUT.unlink()
    if VALID_OUT.exists():
        VALID_OUT.unlink()

    # 1) train
    total_train = 0
    for idx, (url, dest) in enumerate(build_train_urls(), start=1):
        print(f"\n=== TRAIN SHARD {idx}/{TRAIN_SHARDS} ===")
        download_file(url, dest)
        written = append_gzip_jsonl_to_jsonl(dest, TRAIN_OUT)
        total_train += written
        print(f"[merged] {dest.name}: {written} rows")
        print(f"[train total] {total_train}")

    # 2) validation
    print("\n=== VALIDATION ===")
    valid_url, valid_dest = build_validation_url()
    download_file(valid_url, valid_dest)
    total_valid = append_gzip_jsonl_to_jsonl(valid_dest, VALID_OUT)
    print(f"[merged] {valid_dest.name}: {total_valid} rows")

    print("\nDONE")
    print(f"train jsonl: {TRAIN_OUT}")
    print(f"valid jsonl: {VALID_OUT}")
    print(f"train rows : {total_train}")
    print(f"valid rows : {total_valid}")


def show_first_records(path, n=10):
    print("\nFIRST RECORDS:\n")
    with open(path, "r", encoding="utf-8") as f:
        for i in range(n):
            line = f.readline()
            if not line:
                break
            obj = json.loads(line)
            print(f"--- record {i+1} ---")
            print(json.dumps(obj, indent=2, ensure_ascii=False))


if __name__ == "__main__":

    # uncomment to redownload 
    main()

    show_first_records(TRAIN_OUT)
