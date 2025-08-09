
# https://huggingface.co/datasets/sentence-transformers/eli5

import pyarrow.parquet as pq
import pandas as pd


file_path = 'datasets/eli5/pair/train-00000-of-00001.parquet'


if __name__ == "__main__":

    chunk_df = pd.read_parquet(file_path, columns=["question", "answer"])

    first_20 = chunk_df.head(20)

    #print(first_20)

    for idx, row in chunk_df.iterrows():
        question = row["question"]
        answer = row["answer"]
        print(f"{idx}: Q: {question}\n      A: {answer}\n")
        break
