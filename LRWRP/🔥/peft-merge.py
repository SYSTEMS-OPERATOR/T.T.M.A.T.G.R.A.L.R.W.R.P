# Try this. Basic steps are to:
# 1/ load the base model
# 2/ train the base model
# 3/ save the LoRA adapter
# 4/ reload the base model at half/full precision
# 5/ merge the LoRA weights with the base model
# 6/ save

base_model = AutoModelForCausalLM.from_pretrained(“base_model”, load_in_8bit=True, torch_dtype=torch.float16, device_map=“auto”)

base_model = prepare_model_for_int8_training(base_model)

peft_model = get_peft_model(base_model, peft_config)

training_args = TrainingArguments()
trainer = Trainer()
trainer.train()

peft_model.save_pretrained(lora_adapter, save_adapter=True, save_config=True)

model_to_merge = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained(base_model).to(“cuda”), lora_adapter)

merged_model = model_to_merge.merge_and_unload()
merged_model.save_pretrained(merged_model)
