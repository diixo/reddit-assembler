
# https://huggingface.co/datasets/sentence-transformers/eli5

import pyarrow.parquet as pq
import json
import pandas as pd
from collections import Counter
from pathlib import Path
from utils import read_embedded_dict, filter_dictionary, clean_text, str_tokenize_words, save_embedded_dict


path = Path("data/eli5-dictionary-counter.json")


def processing(dictionary: Counter):

    chunk_df = pd.read_parquet("datasets/eli5/pair/train-00000-of-00001.parquet", columns=["question", "answer"])

    first_20 = chunk_df.head(20)

    #print(first_20)

    for idx, row in chunk_df.iterrows():

        question = row["question"]
        answer = row["answer"]
        #print(f"{idx}::question: {question}\nanswer: {answer}")

        if (idx + 1) % 1000 == 0:
            print(f"...items={idx}")

        txt = clean_text(question + " " + answer)

        dictionary.update(str_tokenize_words(txt))

    print(f"total items={idx}")



if __name__ == "__main__":

    dictionary = Counter()

    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            dictionary = Counter(json.load(f))


    embedded_words = read_embedded_dict()

    #processing(dictionary)

    ############# save results

    if len(dictionary.items()) > 0:

        dictionary = Counter(filter_dictionary(dictionary, embedded_words))
        new_dict = dict()

        for word, count in dictionary.items():
            word = word.strip()
            if word not in embedded_words:
                if word.lower() in embedded_words:
                    embedded_words.add(word)
                    #print(f"added: [{word}]")
                else:
                    new_dict[word] = count

        dictionary = Counter(new_dict)
        save_embedded_dict(embedded_words)

        with path.open("w", encoding="utf-8") as f:
            json.dump(dictionary, f, indent=2)
        print(f"Saved json.sz={len(dictionary.items())}")

        most_common = dictionary.most_common()

        sorted_words = [word for word, _ in most_common]
        #sorted_words = sorted([word for word, _ in most_common])


        with open(f"data/eli5-dictionary.txt", "w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")
