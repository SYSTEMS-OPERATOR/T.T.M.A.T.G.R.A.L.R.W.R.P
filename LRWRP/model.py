import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import AdamW
from tqdm import tqdm
import numpy as np

class SubtitleDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def read_srt_file(file_path):
    # Implement your SRT file reading logic here
    # You should return a list of dialogues and a list of corresponding speaker tags
    pass

def encode_labels(labels, label_to_id):
    return [label_to_id[label] for label in labels]

def train(model, data_loader, optimizer):
    model.train()
    for batch in tqdm(data_loader, desc="Training"):
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

def evaluate(model, data_loader):
    model.eval()
    eval_loss = 0
    for batch in tqdm(data_loader, desc="Evaluating"):
        with torch.no_grad():
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            eval_loss += outputs.loss.item()
    return eval_loss / len(data_loader)

# Define your label map based on your SRT file structure
label_to_id = {"O": 0, "B-SPEAKER": 1, "I-SPEAKER": 2}
id_to_label = {id: label for label, id in label_to_id.items()}

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=len(label_to_id))

# Read and process your SRT data
dialogues, speaker_tags = read_srt_file("path_to_your_srt_file.srt")
encoded_input = tokenizer(dialogues, is_split_into_words=True, return_tensors="pt", padding=True, truncation=True)
encoded_labels = encode_labels(speaker_tags, label_to_id)

# Split the dataset
train_texts, val_texts, train_tags, val_tags = train_test_split(dialogues, encoded_labels, test_size=0.2)

# Create Datasets
train_encodings = tokenizer(train_texts, is_split_into_words=True, padding=True, truncation=True)
val_encodings = tokenizer(val_texts, is_split_into_words=True, padding=True, truncation=True)
train_dataset = SubtitleDataset(train_encodings, train_tags)
val_dataset = SubtitleDataset(val_encodings, val_tags)

# DataLoader
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

# Optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)

# Training and Evaluation
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(3):  # Number of training epochs
    print(f"Epoch {epoch+1}")
    train(model, train_loader, optimizer)
    eval_loss = evaluate(model, val_loader)
    print(f"Validation Loss: {eval_loss}")

# Save the model
model.save_pretrained("your_model_directory")
