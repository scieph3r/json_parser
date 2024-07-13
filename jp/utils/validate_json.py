def is_valid(tokens):
    if len(tokens) < 1: return False
    collections = 0
    stack = []
    seen_key = False
    seen_indicator = False
    seen_comma = False
    for token in tokens:
        if token == ",":
            if seen_comma or seen_key:
                return False
            seen_comma = True
        # check for :
        elif token == ":":
            if (not seen_key) or seen_indicator:
                return False
            seen_indicator = True
        # check for valid strings
        elif token[0] == "\"" and token[-1] != "\"":
            return False
        elif token[0] == "\"":
            if not seen_key:
                seen_key = True
                if seen_comma: seen_comma = False
            elif seen_key and not seen_indicator:
                return False
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
        # check lexical balance
        elif token == "{":
            stack.append("}")
        elif token == "[":
            stack.append("]")
        elif token == "}":
            if seen_key or seen_comma:
                return False
            if stack[-1] == "}":
                stack = stack[:-1]
            else:
                return False
        elif token == "]":
            if seen_key or seen_comma:
                return False
            if stack[-1] == "]":
                stack = stack[:-1]
            else:
                return False
        else:
            return False
        
    return True

def tokenize(str):
    stripped_str = str.strip()
    start_tokens = ["{", "[", ":", ","]
    end_tokens = ["}", "]", ":", ","]
    valid_tokens = start_tokens + end_tokens 
    tokens = []
    tmp = ""
    i = 0
    length = len(stripped_str)
    while i < length:
        # handle strings
        if stripped_str[i] == "\"":
            tmp += "\""
            i += 1
            while  i < len(stripped_str) and stripped_str[i] != "\"":
                tmp += stripped_str[i]
                i += 1
            tmp += "\""
            tokens.append(tmp)
            tmp = ""
        # handle special tokens
        elif stripped_str[i] in valid_tokens:
            tokens.append(stripped_str[i])
        i += 1
    if is_valid(tokens):
        return tokens
    else:
        return None
