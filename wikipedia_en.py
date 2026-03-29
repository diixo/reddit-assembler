import os
from collections import Counter
import multiprocessing as mp

from tqdm import tqdm
from datasets import load_dataset

from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("gpt2", use_fast=True)
eot = tokenizer.convert_tokens_to_ids("<|endoftext|>")


def format_tokens(n: int) -> str:
    if n >= 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.2f}T"  # trillion
    elif n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f}B"  # billion
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"  # million
    elif n >= 1_000:
        return f"{n / 1_000:.2f}K"  # thousand
    return str(n)


# use for hugging-face tokenizer
def hf_tokenize_to_len(row):
    # tokenizes a single document and returns a numpy array of uint16 tokens
    ids = tokenizer.encode(row["text"], add_special_tokens=False)

    return len(ids)


if __name__ == "__main__":

    print(format_tokens(4_640_971_626))

    #fw = load_dataset("parquet", data_files="data/legacy-datasets-wikipedia/*.parquet", split="train", streaming=True)

    # 6_458_670 rows
    fw = load_dataset("parquet", data_files="datasets/wikipedia-legacy/*.parquet", split="train", local_files_only=True)

    total_docs = len(fw)

    size_map_counter = Counter()
    nprocs = min(4, os.cpu_count())

    total_tokens = 0

    with mp.Pool(nprocs) as pool:
        with tqdm(total=total_docs, unit="rows") as pbar:
            for token_len in pool.imap(hf_tokenize_to_len, fw, chunksize=16):
                size_map_counter[token_len] += 1
                total_tokens += token_len
                pbar.update(1)

    print(f"\nTokens.all={total_tokens}, nprocs={nprocs}")

