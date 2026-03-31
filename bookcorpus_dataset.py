
# URL = "https://storage.googleapis.com/huggingface-nlp/datasets/bookcorpus/bookcorpus.tar.bz2"

import json
import re
import pandas as pd
from datasets import load_dataset
from pathlib import Path


def load_text(file_path: str, sz = 20):

    items = []

    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue

            item = line

            item = item.replace(" ' ", "'")
            item = item.replace(" ?", "?")
            item = item.replace(" )", ")")
            item = item.replace("( ", "(")
            item = item.replace(" !", "!")
            item = item.replace(" .", ".")
            item = item.replace(" ;", ";")
            item = item.replace(" ,", ",")
            item = item.replace(" ’ ", "'")
            item = item.replace(" / ", "/")
            item = item.replace(" & ", "&")
            #item = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', item)

            items.append(item)

            if (sz > 0) and (sz <= len(items)):
                break
    return items


if __name__ == "__main__":

    output_path = "datasets/bookcorpus/bookcorpus-dedup.jsonl"

    if not Path(output_path).exists():

        txt_1 = load_text("datasets/bookcorpus/books_large_p1.txt", sz=0)

        txt_2 = load_text("datasets/bookcorpus/books_large_p2.txt", sz=0)

        print(len(txt_1) + len(txt_2)) # 74004228

        ###################################################################################

        df = pd.DataFrame({"text": txt_1 + txt_2})

        df_filtered = df.drop_duplicates(subset=["text"]).reset_index(drop=True)

        print("after deduplication sz:", len(df_filtered))

        df_filtered.to_json(output_path, orient="records", lines=True, force_ascii=False)

    else:
        # 38832670
        with open(output_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                record = json.loads(line)
                print(f"--- record {i+1} ---")
                print(record["text"])
