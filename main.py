
# pip install zstandard
import zstandard as zstd

import io
import json


def print_submission(data_obj: dict):
    title = data_obj["title"]
    txt = data_obj["selftext"]
    id = data_obj["id"]
    subreddit = data_obj["subreddit"]
    print(title)
    print(txt)
    print(id)
    print("subreddit:", subreddit)
    print("score:", data_obj["score"])
    print("num_comments:", data_obj["num_comments"])
    print("is_text:", data_obj["is_self"])
    print("18+:", data_obj["over_18"])


def test(file_path: str):

    with open(file_path, 'rb') as compressed:
        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(compressed) as reader:
            text_stream = io.TextIOWrapper(reader, encoding='utf-8')
            for i, line in enumerate(text_stream):

                if i > 0:  # Только первые 10 строк для примера
                   break

                try:
                    data = json.loads(line)
                    #print(data)
                    #print_submission(data)
                except json.JSONDecodeError:
                    print(f"Ошибка при разборе строки {i}: {line[:100]}")

                if i % 1000 == 0 and i > 0:
                    print("total_items:", str(i))
                


if __name__ == "__main__":

    file_path = "C:/utorrent/2025-04/submissions/RS_2025-04.zst"

    test(file_path)
