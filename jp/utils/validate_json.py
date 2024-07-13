def parse_number(num_str):
    # Try to convert the string to an integer
    try:
        return int(num_str)
    except ValueError:
        pass

    # Try to convert the string to a float
    try:
        return float(num_str)
    except ValueError:
        pass

    # If none of the above work, return None
    return None

def is_valid(tokens):
    if len(tokens) < 1: return False
    collections = 0
    stack = []
    seen_key = False
    seen_indicator = False
    seen_comma = False
    for token in tokens:
        if isinstance(token, int) or isinstance(token, float):
            if seen_key and not seen_indicator:
                return False
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
        # check for None, True and False
        elif token == None or token == True or token == False:
            if seen_key and not seen_indicator:
                return False
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
        # check for ,
        elif token == ",":
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
            if len(stack) < 1:
                return False
            if seen_key or seen_comma:
                return False
            if stack[-1] == "}":
                stack = stack[:-1]
            else:
                return False
        elif token == "]":
            if len(stack) < 1:
                return False
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
        # handle null
        elif i + 3 < len(stripped_str) and stripped_str[i: i + 4] == "null":
            tokens.append(None)
        #handle bool
        elif i + 3 < len(stripped_str) and stripped_str[i: i + 4] == "true":
            tokens.append(True)
        elif i + 4 < len(stripped_str) and stripped_str[i: i + 5] == "false":
            tokens.append(False)
        # handle numbers
        elif stripped_str[i].isdigit():
            while stripped_str[i].isdigit() or stripped_str[i] == "." or stripped_str[i] == "e" or stripped_str[i] == "E":
                tmp += stripped_str[i]
                i += 1
            result = parse_number(tmp)
            tmp = ""
            if result != None:
                tokens.append(result)
            continue
        # handle special tokens
        elif stripped_str[i] in valid_tokens:
            tokens.append(stripped_str[i])
        i += 1
    if is_valid(tokens):
        return tokens
    else:
        return None
