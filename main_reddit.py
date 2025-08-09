
# pip install zstandard
import zstandard as zstd

from pathlib import Path
import io
import json
import re
from collections import Counter
import csv
from utils import filter_dictionary, clean_text, str_tokenize_words


class RedditAssembler:

    def __init__(self):

        self.subreddit_counter = Counter()

        path = Path("data/dictionary-counter.json")
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                self.dictionary = Counter(json.load(f))
        else:
            self.dictionary = Counter()

        print(f"Loaded: words dictionary.sz={len(self.dictionary.items())}")

        self.total_count = 0
        self.valid_count = 0


    def add_item(self, data_obj: dict):

        subreddit = data_obj.get("subreddit")
        if subreddit:
            self.subreddit_counter[subreddit] += 1

        self.total_count += 1
        # if self.total_count % 1000 == 0:
        #     print("total_items:", str(self.total_count))

        # check if locked
        locked = "False"
        locked = data_obj.get("locked", locked)

        if bool(locked) == True:
            return

        # valid_count means not locked
        self.valid_count += 1

        title = data_obj.get("title")
        if title:   # submission

            self.dictionary.update(str_tokenize_words(clean_text(title)))

            txt = data_obj.get("selftext")
            if txt:
                self.dictionary.update(str_tokenize_words(clean_text(txt)))

            # num_comments = data_obj.get("num_comments", 0)
            # if int(num_comments) > 0:
            #     self.valid_count += 1

        else:       # comment

            body = data_obj.get("body")
            if body:
                body = clean_text(body)
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


    def save(self, amount=250_000):

        sorted_subreddits = self.subreddit_counter.most_common()

        # print-out only top
        # for subreddit, count in sorted_subreddits[:500]:
        #     print(f"{subreddit}: {count}")

        # with open("data/subreddit-top-500.csv", "w", newline='', encoding="utf-8") as f:
        #     writer = csv.writer(f, delimiter=";")
        #     writer.writerow(["subreddit", "comment_count"])
        #     writer.writerows(sorted_subreddits)

        self.dictionary = Counter(filter_dictionary(self.dictionary))

        print(f"Saved: dictionary.sz={len(self.dictionary.items())}")

        most_common = self.dictionary.most_common(amount)

        with open(f"data/dictionary-top-{amount}.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["word", "count"])
            writer.writerows(most_common)

        sorted_words = [word for word, _ in most_common]

        with open(f"data/dictionary-top-{amount}.txt", "w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")

        print(f"submissions: total={self.total_count}, valid={self.valid_count}, unknown={self.total_count-self.valid_count}")

        if len(self.dictionary.items()) > 0:
            with Path("data/dictionary-counter.json").open("w", encoding="utf-8") as f:
                json.dump(self.dictionary, f, indent=2)


def test_reddit(file_list: list[str], assembler: RedditAssembler):

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
       "C:/utorrent/reddit/2025-03/submissions/RS_2025-03.zst",
       "C:/utorrent/reddit/2025-03/comments/RC_2025-03.zst",
    ]

    assembler = RedditAssembler()

    #test_reddit(file_list, assembler)

    assembler.save()