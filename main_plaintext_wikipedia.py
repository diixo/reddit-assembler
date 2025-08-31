
# https://www.kaggle.com/code/ffatty/concatenateallwikiarticles

import os
from utils import str_tokenize_words


input_dir = './datasets/wikipedia-fullEnglish'
output_dir = './train-results'


def read_from_file(filename):
    f = open(filename, "r", encoding="utf-8")
    words = 0
    lines = f.readlines()
    for line in lines:
        tokens = str_tokenize_words(line)
        words += len(tokens)

    return len(lines), words


if __name__ == "__main__":

    massive_file_path = os.path.join(output_dir, 'plaintext-wikipedia-en.txt')

    intermediate_files = []
    
    walk_list = os.walk(input_dir)

    sents = 0
    words = 0

    for root, _, filenames in walk_list:
        if filenames:
            relative_dir = os.path.relpath(root, input_dir)
            output_file = os.path.join(output_dir, f"{relative_dir.replace(os.sep, '_')}.txt")
            intermediate_files.append(output_file)

            for filename in sorted(filenames):
                file_path = os.path.join(root, filename)
                count_s, count_w = read_from_file(file_path)

                sents += count_s
                words += count_w

            print(f"Read files({len(filenames)}) in {root} [...sents={sents} ...words={words}]")

            #os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # with open(output_file, 'w') as outfile:
            #     for filename in sorted(filenames):
            #         file_path = os.path.join(root, filename)
            #         try:
            #             with open(file_path, 'r') as infile:
            #                 outfile.write(infile.read())
            #                 outfile.write("\n")
            #         except Exception as e:
            #             print(f"Error reading {file_path}: {e}")
            #print(f"Concatenated files in {root} into {output_file}")

    print("sents:", sents, "words:", words) # sents: 79_087_472 words: 1_953_810_569

