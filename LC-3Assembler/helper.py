def decstrToInt(str):
    f = 1
    val = 0
    if str[0] == '-':
        f = -1
        str = str[1:]
    for ch in str:
        if ch >= '0' and ch <= '9':
            val = val * 10
            val += ord(ch) - ord('0')
        else:
            return None
    return f * val

def binstrToInt(str):
    val = 0
    for ch in str:
        if ch >= '0' and ch <= '1':
            val = val << 1
            val += ord(ch) - ord('0')
        else:
            return None
    return val

def hexstrToInt(str):
    val = 0
    for ch in str:
        val = val << 4
        if ch >= '0' and ch <= '9':
            val += ord(ch) - ord('0')
        elif ch >= 'a' and ch <= 'f':
            val += ord(ch) - ord('a') + 10;
        else:
            return None
    return val


def charToInt(str):
    str = lowerCaseWord(str)
    op = str[0]
    str = str[0:]
    val = 0
    if op == '#':
        val = decstrToInt(str[1:])
    elif op == 'b':
        val = binstrToInt(str[1:])
    elif op == 'x':
        val = hexstrToInt(str[1:])
    else:
        val = None
    return val

def lowerCase(word):
    if word >= 'A' and word <= 'Z':
        word = chr(ord(word) + 32)
    return word

def lowerCaseWord(word):
    try:
        res = ''
        for ch in word:
            res += lowerCase(ch)
        return res
    except AttributeError:
        return None

def immOutOfRange(imm, immLen):
    if imm < 0:
        imm = ~imm
    upper = (1 << immLen-1) - 1
    if imm > upper:
        return True
    return False

def validSymbol(str):
    flag = True
    ch = lowerCase(str[0])
    if ch < 'a' or ch > 'z':
        return False
    for ch in str[1:]:
        ch = lowerCase(ch)
        if (ch < 'a' or ch > 'z') and (ch < '0' or ch > '9'):
            return False
    return True
