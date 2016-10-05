import os
import sys
import hashlib
import collections


def hash_file(file_name):
    h = hashlib.md5()
    with open(file_name, "rb") as fd:
        h.update(fd.read())
    return h.hexdigest()


def search_for_duplicates(directory):
    dic = collections.defaultdict(list)
    for roots, _, files in os.walk(directory):
            for f in files:
                path = os.path.join(roots, f)
                h = hash_file(path)
                if not os.path.islink(path) and not f.startswith(('.', '~')):
                    dic[h].append(path)
    return dic

directory = sys.argv[1]
dic = search_for_duplicates(directory)
for value in dic.values():
    if len(value) > 1:
        print(*value, sep=':')
