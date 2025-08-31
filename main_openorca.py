
import torch
from transformers import AutoTokenizer, LlamaTokenizer, LlamaConfig, LlamaForCausalLM, AutoModelForCausalLM
from datasets import load_dataset, Dataset
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from torch.utils.data import DataLoader

from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")



dataset = load_dataset("Open-Orca/OpenOrca", split="train", streaming=False)

print(f"Size: {len(dataset)}")


def count_tokens(example):
    return {
        "n_tokens": sum(len(tokenizer.encode(example[field])) for field in ["system_prompt","question","response"])
    }


#
dataset = dataset.map(count_tokens, batched=False)

#
total_tokens = sum(dataset["n_tokens"])
print(f"Total tokens in DS: {total_tokens}")

# 1_592_792_390
