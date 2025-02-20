#!/bin/bash

# Install huggingface-cli if not already installed
pip install huggingface-cli

# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

# Create models directory if it doesn't exist
mkdir -p models

# Download the model
huggingface-cli download unsloth/DeepSeek-R1-Distill-Qwen-32B-GGUF DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf \
    --local-dir models/

# Run with updated model path
./build/bin/llama-cli \
    --model models/DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf \
    --cache-type-k q8_0 \
    --threads 16 \
    --prompt '<｜User｜>What is 1+1?<｜Assistant｜>' \
    --n-gpu-layers 100 \
    -no-cnv