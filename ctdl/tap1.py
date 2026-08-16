def verifyy(s):
    open = ("(", "[", "{")
    close = (")", "]", "}")
    anhxa ={
        "(" : ")",
        "[" : "]",
        "{" : "}"
    }
    stack = []
    c = 0
    for i in range(len(s)):
        if s[i] in open:
            stack.append(s[i])
            c += 1
        if s[i] in close:
            if anhxa[stack[-1]] == s[i]:
                stack.pop()
                c -= 1
            else: 
                return False
    if c != 0: 
        return False
    return True