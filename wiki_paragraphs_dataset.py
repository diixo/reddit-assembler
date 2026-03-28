
from datasets import load_dataset
from transformers import GPT2TokenizerFast
from tqdm import tqdm


DATASET_NAME = "mamei16/en_wikipedia_paragraphs"
SPLIT = "train"

# Если хочешь быстрый тест, поставь число, например 10000
# Если хочешь считать весь split, оставь None
MAX_SAMPLES = None

# Если знаешь точное имя текстовой колонки, можно вписать сюда.
# Иначе скрипт попробует найти её автоматически.
TEXT_COLUMN = None


def detect_text_column(ds):
    candidates = ["text", "paragraph", "content", "article", "body"]
    print(ds.column_names)
    for c in candidates:
        if c in ds.column_names:
            return c

    # fallback: ищем первую строковую колонку
    sample = ds[0]
    for k, v in sample.items():
        if isinstance(v, str):
            return k

    raise ValueError(f"Не удалось найти текстовую колонку. Доступные колонки: {ds.column_names}")


def main():
    print("Loading dataset...")
    ds = load_dataset(DATASET_NAME, split=SPLIT)

    text_col = TEXT_COLUMN or detect_text_column(ds)
    print(f"Using text column: {text_col}")
    print(f"Dataset rows in split '{SPLIT}': {len(ds)}")

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    total_tokens = 0
    total_chars = 0
    total_samples = 0
    max_tokens_in_sample = 0

    n = len(ds) if MAX_SAMPLES is None else min(MAX_SAMPLES, len(ds))

    for i in tqdm(range(n), desc="Counting GPT-2 tokens"):
        text = ds[i][text_col]

        if not isinstance(text, str):
            continue
        text = text.strip()
        if not text:
            continue

        # add_special_tokens=False чтобы считать именно токены текста,
        # без искусственного BOS/EOS
        ids = tokenizer.encode(text, add_special_tokens=False)

        tok_count = len(ids)
        total_tokens += tok_count
        total_chars += len(text)
        total_samples += 1
        if tok_count > max_tokens_in_sample:
            max_tokens_in_sample = tok_count

    print("\n=== RESULTS ===")
    print(f"Samples processed: {total_samples}")
    print(f"Total GPT-2 tokens: {total_tokens}")
    print(f"Average tokens per sample: {total_tokens / total_samples:.2f}" if total_samples else "Average tokens per sample: n/a")
    print(f"Average chars per sample: {total_chars / total_samples:.2f}" if total_samples else "Average chars per sample: n/a")
    print(f"Average chars per token: {total_chars / total_tokens:.2f}" if total_tokens else "Average chars per token: n/a")
    print(f"Max tokens in one sample: {max_tokens_in_sample}")


if __name__ == "__main__":
    main()
