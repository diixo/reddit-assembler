
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

            if (sz > 0) and (sz <= len(items)):
                break
    return items


if __name__ == "__main__":

    txt = load_text("datasets/bookcorpus/books_large_p1.txt", sz=20)

    print(txt)


    ###################################################################################
    #deduplicate script: https://huggingface.co/datasets/Saibo-creator/bookcorpus_deduplicated

    #dataset = load_dataset("bookcorpus")["train"]["text"]
    # df = pd.Dataframe({"text": dataset})

    # # drop duplicates(exact match)
    # df_filtered = df["text"].drop_duplicates()

    # df_filtered.to_csv("bookcorpus_filtered.csv", "index"=False, "header"=False)
    # new_dataset = load_dataset("text",data_files={"train":"bookcorpus_filtered.csv"})
