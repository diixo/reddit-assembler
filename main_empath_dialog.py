
import json
from datasets import load_dataset
from collections import Counter
from main_owt2 import read_embedded_dict, filter_dictionary, clean_text, str_tokenize_words
from pathlib import Path


path = Path("data/empath-dictionary-counter.json")


def processing(dictionary: Counter):
    dataset = load_dataset("empathetic_dialogues", trust_remote_code=True)

    cntr = 0
    for split in ["train", "validation", "test"]:

        for item in dataset[split]:
            cntr += 1
            if cntr % 1000 == 0:
                print(f"...items={cntr}")

            txt = item["utterance"]
            txt = clean_text(txt.replace("_", " ").replace(":", " ").replace(",", " "))

            dictionary.update(str_tokenize_words(txt))
    # total items = 99646
    print(f"total items={cntr}")


if __name__ == "__main__":

    dictionary = Counter()

    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            dictionary = Counter(json.load(f))


    skip_words = read_embedded_dict()

    #processing(dictionary)

    ############# save results

    if len(dictionary.items()) > 0:
        dictionary = Counter(filter_dictionary(dictionary, skip_words))
        print("Saved json.sz=", len(dictionary.items()))

        with path.open("w", encoding="utf-8") as f:
            json.dump(dictionary, f, indent=2)

    most_common = dictionary.most_common()

    sorted_words = [word for word, _ in most_common]


    with open(f"data/empathic-dialogue-dictionary.txt", "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")


