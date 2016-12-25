def average(lst):
    return sum(lst) / len(lst)


def averages_row(mat):
    return list(map(lambda lst: average(lst), mat))


def find_min_pos(mat):
    minx = 0
    miny = 0
    min = mat[0][0]
    for i, lst in enumerate(mat):
        for j, val in enumerate(lst):
            if val < min:
                min = val
                minx = i
                miny = j
    return minx, miny


def unique(lst):
    used = set()
    for val in lst:
        if val not in used:
            used.add(val)
    return list(used)
