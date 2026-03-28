
import re
import pandas as pd
from datasets import load_dataset


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

            if sz <= len(items):
                break
    return items


if __name__ == "__main__":

    txt = load_text("datasets/bookcorpus/books_large_p1.txt", sz=50)

    print(txt)
