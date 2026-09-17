import ollama

print("before")

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one short sentence.",
        }
    ],
)

print("after")
print(response.message.content)