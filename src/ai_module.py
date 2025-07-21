from openai import OpenAI
import os

'''client = OpenAI(
    api_key = ""
) # o4-mini-2025-04-16'''


# DEEPSEEK
client = OpenAI(
    api_key= "", 
    base_url="https://api.deepseek.com/v1" 
) # deepseek-reasoner

def ai_assistant(prompt: str, model: str = "deepseek-reasoner") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
	temperature = 0.3,
	top_p = 1.0,
    #repetition_penalty = 1.10,
    #do_sample = True,
    #seed= 42,
    )
    return response.choices[0].message.content.strip()

