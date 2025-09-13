import json


def load_txt(file_path: str) -> list:
    items = []
    with open(file_path, 'r') as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            items.append(word)
    return items


if __name__ == "__main__":

    txt = load_txt("data/WordNet/wordnet/verb.exc")

    print(len(txt))

    dictionary = {}

    for line in txt:
        words = line.split(" ")
        assert len(words) > 1

        verbs = []
        verbs = dictionary.get(words[1], [])
        verbs.append(words[0])
        dictionary[words[1]] = verbs

    ########################################
    wordnet = []

    for verb, verbs in dictionary.items():
        wordnet.append({
            "input": f"Forms of word \"{verb}\":",
            "output": " ".join([w for w in verbs]),
            "verbs": [verb] + verbs,
        })

    print("wordnet:", len(wordnet))

    with open("data/wordnet-verb-forms.json", "w", encoding="utf-8") as f:
        json.dump(wordnet, f, ensure_ascii=False, indent=2)
