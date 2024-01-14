from transformers import AutoModelForCausalLM, AutoTokenizer
from safetensors import safe_open
import torch
import os

def load_lora_adjustments(lora_path):
    lora_adjustments = {}
    with safe_open(lora_path, framework="pt", device="cpu") as f:
        for key in f.keys():
            lora_adjustments[key] = f.get_tensor(key)
    return lora_adjustments

def apply_lora_adjustments(model, lora_adjustments):
    # Apply the LORA adjustments to the model.
    for name, param in model.named_parameters():
        if name in lora_adjustments:
            adjustment = lora_adjustments[name]
            param.data = param.data + adjustment

from safetensors import safe_open

def main():
    base_model_dir = "/home/Ubuntu/Desktop/text-generation-webui/models/"
    lora_dir = "/home/Ubuntu/Desktop/UTENA/LORAS"
    local_save_path = "/home/Ubuntu/Desktop/UTENA"

    # Example model and LORA names - replace these with actual file names
    base_model_name = "fblgit_UNA-TheBeagle-7b-v1"
    lora_name = "UNA/adapter_model.safetensors"

    # Construct full paths
    base_model_path = os.path.join(base_model_dir, base_model_name)
    lora_path = os.path.join(lora_dir, lora_name)

    # Load the base model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(base_model_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)

    # Load LORA adjustments
    lora_adjustments = load_lora_adjustments(lora_path)

    # Apply LORA adjustments to the model
    apply_lora_adjustments(model, lora_adjustments)

    # Create directory for saving merged model if it doesn't exist
    if not os.path.exists(local_save_path):
        os.makedirs(local_save_path)

    # Save the merged model locally
    merged_model_path = os.path.join(local_save_path, base_model_name + "-merged")
    model.save_pretrained(merged_model_path)
    tokenizer.save_pretrained(merged_model_path)
    print(f"Merged model saved at {merged_model_path}")

if __name__ == "__main__":
    main()
