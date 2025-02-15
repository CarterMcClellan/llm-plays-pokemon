#!/bin/bash

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-R1-Distill-Qwen-32B-GGUF/DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf \
    --cache-type-k q8_0 \
    --threads 16 \
    --prompt '<｜User｜>What is 1+1?<｜Assistant｜>' \
    -no-cnv