import os
import sys
import hashlib
import collections


def hash_file(file_name):
    h = hashlib.md5()
    with open(file_name, "rb") as fd:
        h.update(fd.read())
    return h.hexdigest()


def search_for_duplicates(top_dir):
    hash_to_files = collections.defaultdict(list)
    for cur_dir, _, files in os.walk(top_dir):
            for f in files:
                absolute_path = os.path.abspath(os.path.join(cur_dir, f))
                if (not f.startswith(('.', '~')) and
                        not os.path.islink(absolute_path)):
                        h = hash_file(absolute_path)
                        hash_to_files[h].append(absolute_path)
    return hash_to_files

directory = sys.argv[1]
hash_to_files = search_for_duplicates(directory)
for files in hash_to_files.values():
    if len(files) > 1:
        print(*files, sep=':')
