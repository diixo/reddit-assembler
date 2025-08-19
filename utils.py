import torch
import re
import html
from pathlib import Path


def str_tokenize_words(s: str):
    s = re.findall("(\.?\w[\w'\.&-]*\w|\w\+*#?)", s)
    if s: return s
    return []


def filter_dictionary(word_counts: dict, skip_words=set()) -> dict:
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
    text = re.sub(r"[-*_.]{2,}", " ", text)

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

    path = Path("data/db-full.txt")
    with path.open("r", encoding="utf-8") as f:
        word_set = set([line.strip() for line in f if line.strip()])
    print(f"db-full.sz={len(word_set)}")
    return word_set


def save_embedded_dict(word_set: set):

    word_list = sorted(word_set)

    path = Path("data/db-full.txt")
    with path.open("w", encoding="utf-8") as f:
        for word in word_list:
            f.write(word + "\n")

    word_dictionary = {
        "iwords": word_list,
        "words": {w: i for i, w in enumerate(word_list)}
    }
    torch.save(word_dictionary, "data/word_dictionary.pth")

    print(f"Saved: db-full.sz={len(word_list)}")

