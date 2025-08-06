import textwrap
import re


def load_prompt(path: str, article_text: str, question: str = "", theme: str = "", keyword: str = "") -> str:
    with open(path, encoding="utf-8") as f:
        template = f.read()
    template = textwrap.dedent(template)
    
    format_dict = {
        'context': article_text,
        'question': question,
        'theme': theme,
        'keyword': keyword
    }
    
    variables_in_template = re.findall(r'\{(\w+)\}', template)
    
    filtered_dict = {}
    for var in variables_in_template:
        if var in format_dict:
            filtered_dict[var] = format_dict[var]
    
    return template.format(**filtered_dict)
