from llama_cpp import Llama

llm = Llama(
      model_path="./models/7B/llama-model.gguf",
)
output = llm(
      "<｜User｜>What is 1+1?<｜Assistant｜>'", # Prompt
      echo=True # Echo the prompt back in the output
) # Generate a completion, can also call create_completion
print(output)