
def load_prompt_template(prompt_template_path: str) -> str:
    with open(prompt_template_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    return prompt_template

