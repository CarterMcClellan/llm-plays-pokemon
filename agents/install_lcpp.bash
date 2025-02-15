#!/bin/bash

# Install huggingface-cli if not already installed
pip install huggingface-cli

# Create models directory if it doesn't exist
mkdir -p models

# Download the model
huggingface-cli download unsloth/DeepSeek-R1-Distill-Qwen-32B-GGUF DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf \
    --local-dir models/

# # Run with updated model path
# ./build/bin/llama-cli \
#     --model models/DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf \
#     --cache-type-k q8_0 \
#     --threads 16 \
#     --prompt '<｜User｜>What is 1+1?<｜Assistant｜>' \
#     --n-gpu-layers 100 \
#     -no-cnv

CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python