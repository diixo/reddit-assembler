
# pip install zstandard
import zstandard as zstd

from pathlib import Path
import io
import json
import re
from collections import Counter
import csv


def str_tokenize_words(s: str):
    s = re.findall("(\.?\w[\w'\.&-]*\w|\w\+*#?)", s)
    if s: return s
    return []


def read_embedded_dict():
    with open("data/db-full.txt", "r", encoding="utf-8") as f:
        word_set = set([line.strip() for line in f if line.strip()])
    print("db-full.SZ=", len(word_set))
    return sorted(word_set)


def clean_gif_links(text):
    # remove constructions like: ![...](giphy|...)
    return re.sub(r"!\[.*?\]\(giphy\|.*?\)", "", text)


class RedditAssembler:

    def __init__(self):

        self.subreddit_counter = Counter()

        path = Path("data/dictionary-counter.json")
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                self.dictionary = Counter(json.load(f))
        else:
            self.dictionary = Counter()

        self.total_count = 0
        self.valid_count = 0


    def add_item(self, data_obj: dict):

        subreddit = data_obj.get("subreddit")
        if subreddit:
            self.subreddit_counter[subreddit] += 1

        self.total_count += 1

        # check if locked
        locked = "False"
        locked = data_obj.get("locked", locked)

        if bool(locked) == True:
            return

        # valid_count means not locked
        self.valid_count += 1

        title = data_obj.get("title")
        if title:   # submission

            self.dictionary.update(str_tokenize_words(title.replace('’', "'")))

            txt = data_obj.get("selftext")
            if txt:
                self.dictionary.update(str_tokenize_words(txt.replace('’', "'")))

            # num_comments = data_obj.get("num_comments", 0)
            # if int(num_comments) > 0:
            #     self.valid_count += 1

        else:       # comment

            body = data_obj.get("body")
            if body:
                body = body.replace('’', "'")
                body = clean_gif_links(body)
                self.dictionary.update(str_tokenize_words(body))

                #print(f"BODY({locked}):{body}")
            # else:
            #     print("ERRORRRRRRRRRRRRRRRRRRRRRRR")

        # id = data_obj["id"]
        # subreddit = data_obj["subreddit"]
        # print(title)
        # print(txt)
        # print(id)
        # print("subreddit:", subreddit)
        # print("score:", data_obj["score"])
        # print("num_comments:", data_obj["num_comments"])
        # print("is_text:", data_obj["is_self"])
        # print("18+:", data_obj["over_18"])


    def save(self):

        sorted_subreddits = self.subreddit_counter.most_common()

        # print-out only top
        # for subreddit, count in sorted_subreddits[:500]:
        #     print(f"{subreddit}: {count}")

        with open("data/subreddit-top-500.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["subreddit", "comment_count"])
            writer.writerows(sorted_subreddits)

        sorted_words = sorted(
            [word for word, _ in self.dictionary.most_common(250000)]
            )

        with open("data/dictionary-top-250000.txt", "w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")

        print(f"submissions: total={self.total_count}, valid={self.valid_count}, unknown={self.total_count-self.valid_count}")

        if len(self.dictionary.items()) > 0:
            with Path("data/dictionary-counter.json").open("w", encoding="utf-8") as f:
                json.dump(self.dictionary, f, indent=2)


def test(file_list: list[str], assembler: RedditAssembler):

    for file_path in file_list:

        with open(file_path, 'rb') as compressed:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(compressed) as reader:
                text_stream = io.TextIOWrapper(reader, encoding='utf-8')
                for i, line in enumerate(text_stream):

                    # if i > 10:
                    #    break

                    try:
                        data = json.loads(line)
                        assembler.add_item(data)
                    except json.JSONDecodeError:
                        print(f"Error parsing string {i}: {line[:100]}")

                    if i % 1000 == 0 and i > 0:
                        print("total_items:", str(i))


if __name__ == "__main__":

    file_list = [
       "C:/utorrent/2025-04/submissions/RS_2025-04.zst",
       "C:/utorrent/2025-04/comments/RC_2025-04.zst",
    ]

    assembler = RedditAssembler()

    test(file_list, assembler)

    assembler.save()
