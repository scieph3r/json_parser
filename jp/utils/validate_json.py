def is_json(str):
    str = str.strip()
    if len(str) < 1: return False
    return (str[0] == "{" and str[-1] == "}") or (str[0] == "[" and str[-1] == "]")