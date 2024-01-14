"""
The code below combines approaches published by both @eugene-yh and @jinyongyoo on Github. 
Thanks for the contributions guys!
"""

import torch
import peft
import json
import shutil
from peft.utils import _get_submodules
import os
import bitsandbytes as bnb
from bitsandbytes.functional import dequantize_4bit
from peft import PeftModel
from transformers import AutoModelForCausalLM, LlamaForCausalLM, LlamaTokenizer, BitsAndBytesConfig, CodeLlamaTokenizer
import gc
import copy

def save_model(model, tokenizer, to):
    print(f"Saving dequantized model to {to}...")
    model.save_pretrained(to)
    tokenizer.save_pretrained(to)
    config_data = json.loads(open(os.path.join(to, 'config.json'), 'r').read())
    config_data.pop("quantization_config", None)
    config_data.pop("pretraining_tp", None)
    with open(os.path.join(to, 'config.json'), 'w') as config:
        config.write(json.dumps(config_data, indent=2))
    
def dequantize_model(model, tokenizer, to='./dequantized_model', dtype=torch.bfloat16, device="cpu"):
    """
    'model': the peftmodel you loaded with qlora.
    'tokenizer': the model's corresponding hf's tokenizer.
    'to': directory to save the dequantized model
    'dtype': dtype that the model was trained using
    'device': device to load the model to
    """

    # Delete the model object if it exists
    if os.path.exists(to):
        shutil.rmtree(to)

    os.makedirs(to, exist_ok=True)

    cls = bnb.nn.Linear4bit

    with torch.no_grad():
        for name, module in model.named_modules():
            if isinstance(module, cls):
                print(f"Dequantizing `{name}`...")
                quant_state = copy.deepcopy(module.weight.quant_state)

                quant_state[2] = dtype

                weights = dequantize_4bit(module.weight.data, quant_state=quant_state, quant_type="nf4").to(dtype)

                new_module = torch.nn.Linear(module.in_features, module.out_features, bias=None, dtype=dtype)
                new_module.weight = torch.nn.Parameter(weights)
                new_module.to(device=device, dtype=dtype)

                parent, target, target_name = _get_submodules(model, name)
                setattr(parent, target_name, new_module)

        model.is_loaded_in_4bit = False

        save_model(model, tokenizer, to)
        
        return model
        

model_path = 'Huggingface-base-model/path-goes-here'
adapter_path = 'Huggingface-adapter/path-goes-here'

quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

try:
    print(f"Starting to load the model {model_path} into memory")

    model = LlamaForCausalLM.from_pretrained(
        model_path,
        load_in_4bit=True,
        torch_dtype=torch.bfloat16,
        quantization_config=quantization_config,
        device_map="auto"
    )
    print(model)
    tok = LlamaTokenizer.from_pretrained(model_path)
    
    # Note: This function outputs the dequantized model without merging the adapter yet
    # The code below it will merge the adapter and then save it to disk
    model = dequantize_model(model, tok, to='output-folder-for-dequantized-model-here')
    
    print(model)
    model = PeftModel.from_pretrained(model = model, model_id = adapter_path)
    print(model)
    model = model.merge_and_unload()
    print(model)
    
    print(f"Successfully loaded the model {model_path} into memory")
    
    # Note that the output folder here should be different than the one you used for dequantize_model
    # This save will output the model merged with LoRA weights
    save_model(model, tok, "put-output-folder-here")
    
    print(f"Successfully saved merged model {model_path} to disk")

except Exception as e:
    print(f"An error occurred: {e}")

    # Delete the model object if it exists
    if 'model' in locals():
        del model

    # Clear the GPU cache
    torch.cuda.empty_cache()

    # Run the garbage collection
    gc.collect()

    print("Model, GPU cache, and garbage have been cleared.")
