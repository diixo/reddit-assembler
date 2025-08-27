
import torch
from pathlib import Path
import json


filename = "empatheticdialogues/fb-reddit-dictionary-250k"


def main():

    # model.mdl from EmpatheticDialogues
    saved_params = torch.load("datasets/normal_transformer_finetuned.mdl", map_location=lambda storage, loc: storage)

    dictionary = saved_params["word_dict"]  # dictionary = { words={}, iwords=[], wordcounts=[] }

    word_list = dictionary["iwords"][:250_000]
    word_dict = dictionary["words"]
    wordcounts = dictionary["wordcounts"].tolist()[:250_000]

    assert len(word_list) == len(wordcounts), str(len(wordcounts))


    path = Path(f"data/{filename}.txt")
    with path.open("w", encoding="utf-8") as f:
        for word in word_list:
            f.write(word + "\n")
        f.flush()


    with Path(f"data/{filename}.json").open("w", encoding="utf-8") as f:
        json.dump(dict(zip(word_list, wordcounts)), f, indent=2)


    pt_dictionary = {
        "iwords": word_list,
        "words": { w: word_dict[w] for i, w in enumerate(word_list) }
    }
    torch.save(pt_dictionary, f"data/{filename}.pth")


if __name__ == "__main__":
    main()
