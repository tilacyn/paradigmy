def make_plural(s):
    if(s[-1] == 's' or s[-1] == 'h' and s[-2] == 's' or s[-1] == 'o'):
        return s + 'es'
    if(s[-1] == 'y'):
        return s[:-1] + 'ies'
    return s + 's'


def get_hash_tag(s):
    open_ht = s.find('{')
    if(open_ht == -1):
        return s
    else:
        close_ht = s.find('}', open_ht)
        if(close_ht == -1 or close_ht == open_ht + 1):
            return s
        else:
            return s[open_ht + 1:close_ht]


def tokenize(s):
    i = 0
    res = []
    flag = 0
    while i < len(s):
        in_open = s.find('<', i)
        in_close = s.find('>', i)
        if in_open == -1 or in_close == -1:
            break
        if(not flag):
            res.extend(s[i:in_open].split(' '))
        in_open2 = s.find('<', in_close)
        in_close2 = s.find('>', in_close)
        if in_open2 == -1 or in_close2 == -1:
            in_open2 = len(s)
        in_space = s.find(' ', in_close)
        if in_space == -1 and in_open2 != len(s) or in_space > in_open2:
            res[-1] += s[in_open + 1:in_close] + s[in_close + 1:in_open]
            i = in_open2
            flag = 1
        if in_space < in_open2 and in_space != -1:
            res[-1] += s[in_open + 1:in_close] + s[in_close + 1:in_space]
            i = in_space + 1
            flag = 0
        if in_space == -1 and in_open2 == len(s):
            res[-1] += s[in_open + 1:in_close] + s[in_close + 1:]
            i = len(s)
            break
    if(i != len(s)):
        res.extend(s[i:].split(' '))
    return res
