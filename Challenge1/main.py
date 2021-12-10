mapping_bracket = {
    '{':'}',
    '(':')',
    '[':']'
}

def check_invalid(st,b):
    if not len(st):
        return False
    if mapping_bracket[st[len(st)-1]] == b:
        return True
    return False

def process(a):
    stack = []
    result = True
    if len(a) == 0:
        return False
    for it in a:
        if it in ['}',')',']']:
            if check_invalid(stack,it):
                stack.pop()
            else:
                result = False
                break
        else:
            stack.append(it)
    if result and len(stack) == 0:
        return True
    return False

if __name__ == "__main__":
    string = input()
    a = list(filter(lambda x : x in ['{','}','(',')','[',']'],list(string)))
    if process(a):
        print('Right')
    else:
        print('Wrong')