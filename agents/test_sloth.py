from unsloth import FastLanguageModel
from transformers import TextStreamer

max_seq_length = 2048 
dtype = None 
load_in_4bit = True 
model_name = "unsloth/DeepSeek-R1-Distill-Qwen-32B-bnb-4bit"
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)
FastLanguageModel.for_inference(model) # Enable native 2x faster inference

inputs = tokenizer(
[
    "Hello, how are you?"
], return_tensors = "pt").to("cuda")

text_streamer = TextStreamer(tokenizer)
_ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 128)