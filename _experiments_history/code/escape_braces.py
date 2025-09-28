import json


def normal_load_json_in_markdown(json_dict: dict) -> str:
    return '```json\n' + json.dumps(json_dict, ensure_ascii=False) + '\n```'


def escape_braces(string) -> str:
    # 先将所有的 { } 替换为 {{ }}，然后再处理单独的 { 或者 }
    string = string.replace("{", "{{").replace("}", "}}")
    return string


def json_escape_braces(json_dict: dict) -> str:
    json_str = '```json\n' + json.dumps(json_dict, ensure_ascii=False) + '\n```'
    result = escape_braces(json_str)
    return result

