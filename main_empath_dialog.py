
import re
from datasets import load_dataset
from collections import Counter


def str_tokenize_words(s: str):
    s = re.findall("(\.?\w[\w'\.&-]*\w|\w\+*#?)", s)
    if s: return s
    return []


if __name__ == "__main__":

    dictionary = Counter()

    dataset = load_dataset("empathetic_dialogues", trust_remote_code=True)

    # train = dataset["train"]
    # valid = dataset["validation"]
    # test = dataset["test"]

    cntr = 0

    for split in ["train", "validation", "test"]:

        for item in dataset[split]:
            cntr += 1
            if cntr % 1000 == 0:
                print(f"...items={cntr}")

            txt = item["utterance"]

            dictionary.update(str_tokenize_words(txt))

            most_common = dictionary.most_common()

            sorted_words = [word for word, _ in most_common]


    with open(f"data/emphatic-dialogue-dictionary.txt", "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")

    # total = 99646
    print(f"total items={cntr}")
