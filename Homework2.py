import os
import sys
import hashlib


def hashfile(filename):
    h = hashlib.md5()
    with open(filename, "rb") as fd:
        h.update(fd.read())
    return h.hexdigest()


def dublicate(Directory):
    dic = {}
    for path in os.walk(Directory):
        for files in path[2]:
            h = hashfile(path[0]+'\\'+files)
            if files[0] != '.' and files[0] != '~':
                if dic.get(h):
                    dic[h].extend([files])
                else:
                    dic[h] = [files]
    return dic

Directory = input()
dic = dublicate(Directory)
for key in dic:
    if len(dic[key]) > 1:
        print(*dic[key], sep=':')

