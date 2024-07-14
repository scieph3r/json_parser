from string import printable

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
    if not tokens or len(tokens) < 1: raise SyntaxError(f"No tokens recieved")
    collections = 0
    stack = []
    seen_key = False
    seen_indicator = False
    seen_comma = False
    for token in tokens:
        # check for numbers
        if isinstance(token, int) or isinstance(token, float):
            if len(stack) and stack[-1] == "]":
                seen_comma = False
            elif seen_key and not seen_indicator:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
        # check for None, True and False
        elif token == None or token == True or token == False:
            if seen_key and not seen_indicator:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
        # check for ,
        elif token == ",":
            if seen_comma or seen_key:
                if len(stack) and stack[-1] != "]":
                    raise SyntaxError(f"Unexpected token: {token}")
            seen_comma = True
        # check for :
        elif token == ":":
            if (not seen_key) or seen_indicator:
                raise SyntaxError(f"Unexpected token: {token}")
            seen_indicator = True
        # check for valid strings
        elif token[0] == "\"" and token[-1] != "\"":
            raise SyntaxError(f"Unexpected token: {token}")
        elif token[0] == "\"":
            if not seen_key and len(stack) and stack[-1] != "]":
                seen_key = True
                if seen_comma: seen_comma = False
            elif seen_key and not seen_indicator:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
            if len(stack) and stack[-1] == "]" and seen_comma:
                seen_comma = False
        # check lexical balance
        elif token == "{":
            if seen_key and not seen_indicator:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
            stack.append("}")
        elif token == "[":
            if seen_key and not seen_indicator:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_key and seen_indicator:
                seen_key = False
                seen_indicator = False
            stack.append("]")
        elif token == "}":
            if len(stack) < 1:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_key or seen_comma:
                raise SyntaxError(f"Unexpected token: {token}")
            elif len(stack) and stack[-1] == "}":
                stack = stack[:-1]
                if len(stack) == 0:
                    collections += 1
            else:
                raise SyntaxError(f"Unexpected token: {token}")
        elif token == "]":
            if len(stack) < 1:
                raise SyntaxError(f"Unexpected token: {token}")
            elif seen_comma:
                raise SyntaxError(f"Unexpected token: {token}")
            elif len(stack) and stack[-1] == "]":
                stack = stack[:-1]
                if len(stack) == 0:
                    collections += 1
            else:
                raise SyntaxError(f"Unexpected token: {token}")
        else:
            raise SyntaxError(f"Invalid token: {token}")
    # check for single wrapper
    return collections == 1

def tokenize(str):
    stripped_str = str.strip()
    start_tokens = ["{", "[", ":", ","]
    end_tokens = ["}", "]", ":", ","]
    valid_tokens = start_tokens + end_tokens
    invalid_tokens = [x for x in list(printable) if x not in valid_tokens + [" ", "\t", "\n", "\r", "\x0b", "\x0c"]]
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
            i += 4
            continue
        #handle bool
        elif i + 3 < len(stripped_str) and stripped_str[i: i + 4] == "true":
            tokens.append(True)
            i += 4
            continue
        elif i + 4 < len(stripped_str) and stripped_str[i: i + 5] == "false":
            tokens.append(False)
            i += 5
            continue
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
        elif stripped_str[i] in invalid_tokens:
            message = ""
            if i <= 10:
                message += str[:i]
            else:
                message += str[i - 10: i]
            if i + 10 >= len(str):
                message += str[i:len(str) - i]
            else:
                message += str[i:i + 10]
            raise SyntaxError(f"Unexpected syntax: {message}")
        i += 1
    return tokens

def parse_list(tokens):
    """
    parse a list from a list of tokens
    """
    lst = []
    i = 0
    while i < len(tokens):
        if tokens[i] != "{" and tokens[i] != "[":
                if isinstance(tokens[i], str):
                    lst.append(tokens[i][1:-1])
                else:
                    lst.append(tokens[i])
                i += 1
        else:
            stack = []
            to_parse = []         
            if tokens[i] == "{":
                stack.append("}")
                i += 1
                while True:
                    if tokens[i] == "{":
                        stack.append("}")
                    elif tokens[i] == "[":
                        stack.append("]")
                    elif tokens[i] == "]":
                        stack = stack[:-1]
                    elif tokens[i] == "}":
                        stack = stack[:-1]
                        if len(stack) == 0:
                            i += 1
                            break
                    to_parse.append(tokens[i])
                    i += 1
                lst.append(parse_dict(to_parse))
            else:
                stack.append("]")
                i += 1
                while True:
                    if tokens[i] == "{":
                        stack.append("}")
                    elif tokens[i] == "[":
                        stack.append("]")
                    elif tokens[i] == "]":
                        stack = stack[:-1]
                        if len(stack) == 0:
                            i += 1
                            break
                    elif tokens[i] == "}":
                        stack = stack[:-1]
                    to_parse.append(tokens[i])
                    i += 1
                lst.append(parse_list(to_parse))
        i += 1
    return lst

def parse_dict(tokens):
    """
    parse a dictionary from a list of tokens
    """
    dictionary = {}
    current_key = None
    i = 0
    while i < len(tokens):
        if current_key == None:
            current_key = tokens[i][1:-1]
            i += 1
        else:
            if tokens[i] != "{" and tokens[i] != "[":
                if isinstance(tokens[i], str):
                    dictionary[current_key] = tokens[i][1:-1]
                else:
                    dictionary[current_key] = tokens[i]
            else:
                stack = []
                to_parse = []         
                if tokens[i] == "{":
                    stack.append("}")
                    i += 1
                    while True:
                        if tokens[i] == "{":
                            stack.append("}")
                        elif tokens[i] == "[":
                            stack.append("]")
                        elif tokens[i] == "]":
                            stack = stack[:-1]
                        elif tokens[i] == "}":
                            stack = stack[:-1]
                            if len(stack) == 0:
                                break
                        to_parse.append(tokens[i])
                        i += 1
                    dictionary[current_key] = parse_dict(to_parse)
                else:
                    stack.append("]")
                    i += 1
                    while True:
                        if tokens[i] == "{":
                            stack.append("}")
                        elif tokens[i] == "[":
                            stack.append("]")
                        elif tokens[i] == "]":
                            stack = stack[:-1]
                            if len(stack) == 0:
                                break
                        elif tokens[i] == "}":
                            stack = stack[:-1]
                        to_parse.append(tokens[i])
                        i += 1
                    dictionary[current_key] = parse_list(to_parse)
            current_key = None
            i += 1
        i += 1
    return dictionary
    

def parse_json(str):
    """
    Parse a json object from a list of tokens
    """
    dic = {"data": None}
    tokens = tokenize(str)
    if is_valid(tokens):
        if tokens[0] == "{":
            dic["data"] = parse_dict(tokens[1:-1])
        else:
            dic["data"] = parse_list(tokens[1:-1])

    return dic