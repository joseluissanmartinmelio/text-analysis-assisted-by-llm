import textwrap

def load_prompt(path: str, article_text: str) -> str:
    with open(path, encoding="utf-8") as f:
        template = f.read()
    template = textwrap.dedent(template)
    return template.format(context=article_text)
