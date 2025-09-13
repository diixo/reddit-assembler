

def load_txt(file_path: str) -> list:
    items = []
    with open(file_path, 'r') as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            items.append((word, word))
    return items


if __name__ == "__main__":

    txt = load_txt("data/WordNet/wordnet/verb.exc")

    print(len(txt))
