import os
import sys
import hashlib
import collections


def hash_file(file_name):
    h = hashlib.md5()
    with open(file_name, "rb") as fd:
        h.update(fd.read())
    return h.hexdigest()


def seek_for_duplicates(Directory):
    dic = collections.defaultdict(list)
    for roots, dirs, files in os.walk(Directory):
        for f in files:
            path = os.path.join(roots, f)
            h = hash_file(path)
            if not os.path.islink(path) and not f.startswith('.' or '~'):
                dic[h].extend([f])
    return dic

Directory = input()
dic = seek_for_duplicates(Directory)
for value in dic.values():
    if(len(value) > 1):
        print(*value, sep=':')
