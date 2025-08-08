
import re
from datasets import load_dataset
from collections import Counter
from main_owt2 import read_embedded_dict, clean_text


def str_tokenize_words(s: str):
    s = re.findall("(\.?\w[\w'\.&-]*\w|\w\+*#?)", s)
    if s: return s
    return []


if __name__ == "__main__":

    skip_words = read_embedded_dict()

    dictionary = Counter()

    dataset = load_dataset("empathetic_dialogues", trust_remote_code=True)

    cntr = 0
    for split in ["train", "validation", "test"]:

        for item in dataset[split]:
            cntr += 1
            if cntr % 1000 == 0:
                print(f"...items={cntr}")

            txt = item["utterance"]
            txt = clean_text(txt.replace("_", " "))

            dictionary.update(str_tokenize_words(txt))

            most_common = dictionary.most_common()

            sorted_words = [word for word, _ in most_common if word not in skip_words]


    with open(f"data/empathic-dialogue-dictionary.txt", "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")

    # total items = 99646
    print(f"total items={cntr}")
