
# https://www.kaggle.com/code/ffatty/concatenateallwikiarticles

import os
from utils import str_tokenize_words
from transformers import GPT2Tokenizer


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


input_dir = "./datasets/wikipedia-fullEnglish"
output_dir = "./train-results"
output_file = "plaintext-wikipedia-en.txt"


if __name__ == "__main__":

    massive_file_path = os.path.join(output_dir, 'plaintext-wikipedia-en.txt')

    intermediate_files = []
    
    walk_list = os.walk(input_dir)

    sents = 0
    words = 0
    max_words = 0
    gpt_tokens = 0

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, output_file), 'w', encoding="utf-8") as outfile:

        for root, _, filenames in walk_list:
            if filenames:
                relative_dir = os.path.relpath(root, input_dir)
                output_file = os.path.join(output_dir, f"{relative_dir.replace(os.sep, '_')}.txt")
                intermediate_files.append(output_file)

                for filename in sorted(filenames):
                    file_path = os.path.join(root, filename)

                    f = open(file_path, "r", encoding="utf-8")
                    lines = f.readlines()
                    for line in lines:
                        tokens = str_tokenize_words(line)
                        words += len(tokens)
                        max_words = max(max_words, len(tokens))

                        tokens = tokenizer.encode(line)
                        gpt_tokens += len(tokens)

                        outfile.write(line.strip())
                        outfile.write("\n")

                    outfile.flush()
                    sents += len(lines)

                print(f"Read files({len(filenames)}) in: {root} [...sents={sents} ...words={words}]")
    ################################################################################################
    print(
        "sents:", sents,
        "gpt-tokens:", gpt_tokens,
        "words:", words,
        "max_words_sent:", max_words,
        "avg_words_sent:", int(words/sents + 1)) # sents: 79_087_472 words: 1_953_810_569
