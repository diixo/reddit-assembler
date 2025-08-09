
# pip install zstandard
import zstandard as zstd

from pathlib import Path
import io
import json
import re
from collections import Counter
import csv
import html


def filter_dictionary(word_counts: dict, skip_words: set) -> dict:
    """
    Filters a dictionary, keeping only the words that:
    - may optionally start with a dot
    - contain Latin letters, digits, hyphens, or apostrophes
    - may end with one or more '+' or '#' characters
    - exclude words that start with a dot and contain only digits (with optional '+' or '#' at the end)

    Args:
        word_counts (dict): a dictionary of the form {word: count}

    Returns:
        dict: the filtered dictionary
    """
    # Main filter template
    allowed_pattern = re.compile(r"^\.?[A-Za-z0-9'-]+[+#]*$")

    # Template "bad" words: start with a dot and then only numbers, '+' or '#'
    starts_with_dot_and_digits_only = re.compile(r"^\.[0-9]+[+#]*$")
    digits_only = re.compile(r"^[0-9]+$")

    return {
        word: count
        for word, count in word_counts.items()
        if allowed_pattern.fullmatch(word)
        and not starts_with_dot_and_digits_only.fullmatch(word)
        and not digits_only.fullmatch(word)
        and word not in skip_words
    }


def str_tokenize_words(s: str):
    s = re.findall("(\.?\w[\w'\.&-]*\w|\w\+*#?)", s)
    if s: return s
    return []


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remkved removing and empty comments
    text = text.strip()
    if text.lower() in ("[deleted]", "[removed]", ""):
        return ""

    # Edit HTML entities (&amp;, &gt; etc..)
    text = html.unescape(text)

    # Remove Markdown-graphics like: ![...](giphy|...)
    text = re.sub(r"!\[.*?\]\(giphy\|.*?\)", "", text)

    # Remove markdown-links like: [text](url)
    text = re.sub(r"\[([^\]]+)\]\((https?:\/\/[^\)]+)\)", r"\1", text)

    # Remove bare-links (http/https/ftp)
    text = re.sub(r"(https?|ftp):\/\/\S+", "", text)

    # Remove citates (strings, started with >)
    text = re.sub(r"(?m)^>.*$", "", text)

    # Remove horizontal lines (--- or ***)
    text = re.sub(r"[-*_.]{2,}", "", text)

    # Remove markdown-bold and italic
    text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", text)  # *bold*, **bold**
    text = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", text)     # _italic_, __bold__

    # Remove spaces
    text = re.sub(r"\s{2,}", " ", text)

    # Remove spaces from start-end sentences
    text = text.strip()

    return text.replace('’', "'")



def read_embedded_dict() -> set:
    word_set = set()
    with open("data/db-full.txt", "r", encoding="utf-8") as f:
        word_set = set([line.strip() for line in f if line.strip()])
    print(f"db-full.sz={len(word_set)}")
    return word_set


class RedditAssembler:

    def __init__(self):

        self.subreddit_counter = Counter()

        path = Path("data/owt2-dictionary-counter.json")
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                self.dictionary = Counter(json.load(f))
        else:
            self.dictionary = Counter()

        print(f"Loaded: words dictionary.sz={len(self.dictionary.items())}")

        self.total_count = 0
        self.valid_count = 0
        self.dict_standard = read_embedded_dict()


    def add_item(self, data_obj: dict):

        self.total_count += 1

        # meta = data_obj.get("meta")
        # if meta:
        #     lang = meta.get("lang")
        #     if lang == "en":
        #         self.valid_count += 1

        txt = data_obj.get("text")
        if txt:
            txt = clean_text(txt)
            self.dictionary.update(str_tokenize_words(txt))

        if self.total_count % 1000 == 0:
            print("total_items:", str(self.total_count))



    def save(self, amount=250_000):

        self.dictionary = Counter(filter_dictionary(self.dictionary, self.dict_standard))

        print(f"Saved: dictionary.sz={len(self.dictionary.items())}")

        if len(self.dictionary.items()) > 0:
            with Path("data/owt2-dictionary-counter.json").open("w", encoding="utf-8") as f:
                json.dump(self.dictionary, f, indent=2)

        #################################################

        most_common = self.dictionary.most_common(amount)

        with open(f"data/owt2-dictionary-top-{amount}.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["word", "count"])
            writer.writerows(most_common)

        sorted_words = [word for word, _ in most_common]

        with open(f"data/owt2-dictionary-top-{amount}.txt", "w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")

        print(f"Processed (items): total={self.total_count}, en={self.valid_count}, unknown={self.total_count-self.valid_count}")



def test_owt2(file_list: list[str], assembler: RedditAssembler):

    for file_path in file_list:

        with open(file_path, 'rb') as compressed:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(compressed) as reader:
                text_stream = io.TextIOWrapper(reader, encoding='utf-8')
                for i, line in enumerate(text_stream):

                    # if i > 1:
                    #    break

                    try:
                        data = json.loads(line)
                        assembler.add_item(data)
                    except json.JSONDecodeError:
                        print(f"Error parsing string {i}: {line[:100]}")



if __name__ == "__main__":

    dir_owt2 = "datasets/openwebtext2/"

    list_2006 = [
       f"{dir_owt2}2005-06.jsonl.zst",
       f"{dir_owt2}2005-07.jsonl.zst",
       f"{dir_owt2}2005-08.jsonl.zst",
       f"{dir_owt2}2005-09.jsonl.zst",
       f"{dir_owt2}2005-10.jsonl.zst",
       f"{dir_owt2}2005-11.jsonl.zst",
       f"{dir_owt2}2005-12.jsonl.zst",
    ]

    list_2020 = [
       f"{dir_owt2}2020-01.jsonl.zst",
       f"{dir_owt2}2020-02.jsonl.zst",
       f"{dir_owt2}2020-03.jsonl.zst",
       f"{dir_owt2}2020-04.jsonl.zst",
    ]

    file_list = []
    for year in range(2006, 2020):
        file_list.append(f"{dir_owt2}{str(year)}-01.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-02.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-03.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-04.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-05.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-06.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-07.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-08.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-09.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-10.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-11.jsonl.zst")
        file_list.append(f"{dir_owt2}{str(year)}-12.jsonl.zst")

    file_list = list_2006 + file_list + list_2020
    #print(file_list)

    assembler = RedditAssembler()

    #test_owt2(file_list, assembler)

    assembler.save()
