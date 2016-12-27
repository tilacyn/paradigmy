def make_plural(s):
    if s.endswith('s') or s.endswith('sh') or s.endswith('o'):
        return s + 'es'
    if s.endswith('y'):
        return s[:-1] + 'ies'
    return s + 's'


def get_hash_tag(s):
    open_ht = s.find('{')
    if open_ht == -1:
        return s
    else:
        close_ht = s.find('}', open_ht)
        if close_ht == -1 or close_ht == open_ht + 1:
            return s
        else:
            return s[open_ht + 1:close_ht]


def tokenize(s):
    isopen = False
    res = ['']
    for c in s:
        if c == ' ' and not isopen:
            res.append('')
        elif c == '<':
            isopen = True
        elif c == '>' and isopen:
            isopen = False
        else:
            res[-1] = res[-1] + c
    return res
