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
    hash_to_files = collections.defaultdict(list)
    for roots, _, files in os.walk(directory):
            for f in files:
                path = os.path.join(roots, f)
                h = hash_file(path)
                if not f.startswith(('.', '~')) and not os.path.islink(path):
                    hash_to_files[h].append(path)
    return hash_to_files

directory = sys.argv[1]
hash_to_files = search_for_duplicates(directory)
for files in hash_to_files.values():
    if len(files) > 1:
        print(*files, sep=':')
