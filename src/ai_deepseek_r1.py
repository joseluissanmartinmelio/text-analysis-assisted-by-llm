from openai import OpenAI
import os

api_key = os.environ.get("OPENROUTER_API_KEY")

base_url = "https://openrouter.ai/api/v1"

site_url = "http://localhost:8000"
app_name = "claude-jose"

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
    default_headers={
        "HTTP-Referer": site_url,
        "X-Title": app_name,
    },
)


def ai_assistant(prompt: str, model: str = "deepseek/deepseek-r1-0528:free") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        top_p=1.0,
        # seed= 42,
    )
    return response.choices[0].message.content.strip()
