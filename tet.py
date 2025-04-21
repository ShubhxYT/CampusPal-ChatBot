# Set device
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

from datasets import load_dataset
import pprint as pp
print("Loading the dataset...")
dataset = load_dataset("json", data_files="test.jsonl", split="train")
pp.pprint(dataset)

print(type(dataset))
#decrease the size of the dataset to 10%
dataset = dataset.select(range(int(len(dataset) * 0.1)))
pp.pprint(dataset)