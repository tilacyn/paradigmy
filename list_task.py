def average(lst):
    sum = 0
    for val in lst:
        sum += val
    return sum // len(lst)


def averages_row(mat):
    av_lst = []
    for lst in mat:
        av_lst.append(average(lst))
    return av_lst


def find_min_pos(mat):
    minx = -1
    miny = -1
    min = 200
    for lst in mat:
        for val in lst:
            if val < min:
                min = val
                minx = mat.index(lst)
                miny = lst.index(val)
    return (minx, miny,)


def unique(lst):
    unique_lst = []
    i = 0
    for val in lst:
        if i == lst.index(val):
            unique_lst.append(val)
        i += 1
    return unique_lst
