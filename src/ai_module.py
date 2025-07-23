from openai import OpenAI
import os

'''client = OpenAI(
    api_key = "Your api key"
) # o4-mini-2025-04-16'''


# DEEPSEEK
client = OpenAI(
    api_key= "Your api key", 
    base_url="https://api.deepseek.com/v1" 
) # deepseek-reasoner

def ai_assistant(prompt: str, model: str = "deepseek-reasoner") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
	temperature = 0.1,
	top_p = 1.0,
    seed= 42,
    )
    return response.choices[0].message.content.strip()

