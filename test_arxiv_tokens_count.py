from transformers import GPT2Tokenizer
import json


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def count_tokens_in_jsonl(file_path):
    total_tokens = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)

            title = data.get("title", "") + " "
            description = data.get("description", "")
            tokens = tokenizer.encode(title + description)
            total_tokens += len(tokens)
            if total_tokens > 0:
                if total_tokens % 1_000_000 == 0:
                    print(f"...tokens({file_path}):", total_tokens)
    return total_tokens


dir = "datasets/arxiv-corpus/"
file1 = "arxiv_cs_2015_2020.jsonl"
file2 = "arxiv_cs_2021_2024.jsonl"

tokens_file1 = count_tokens_in_jsonl(dir + file1)
tokens_file2 = count_tokens_in_jsonl(dir + file2)


print(f"Total: {tokens_file1 + tokens_file2}")
# 346_372_409
