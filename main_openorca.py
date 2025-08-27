
import torch
from transformers import AutoTokenizer, LlamaTokenizer, LlamaConfig, LlamaForCausalLM, AutoModelForCausalLM
from datasets import load_dataset, Dataset
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from torch.utils.data import DataLoader


dataset = load_dataset("Open-Orca/OpenOrca", split="train", streaming=False)

print(f"Size: {len(dataset)}")
