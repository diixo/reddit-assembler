
import re
from datasets import load_dataset
from collections import Counter
from main_owt2 import read_embedded_dict, filter_dictionary, clean_text, str_tokenize_words



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
            txt = clean_text(txt.replace("_", " ").replace(":", " ").replace(",", " "))

            # tokens = str_tokenize_words(txt)
            # if "17051" in set(tokens):
            #     original = item["utterance"]
            #     print(original)
            #     print(64*"*"+"\n", txt)

            dictionary.update(str_tokenize_words(txt))
            dictionary = Counter(filter_dictionary(dictionary, skip_words))

            most_common = dictionary.most_common()

            sorted_words = [word for word, _ in most_common]


    with open(f"data/empathic-dialogue-dictionary.txt", "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")

    # total items = 99646
    print(f"total items={cntr}")
