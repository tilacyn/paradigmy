def remove_adjacent(s):
    s1[]
    i=0
    s1.append(s[0])
    while (i<len(s)):
        if(s[i]!=s[i-1]):
            s1.append(s[i])
        i=i+1
            
            
    return s1


def linear_merge(lst1, lst2):
    s=[]
    i=0
    j=0
    while(i<len(lst1) and j<len(lst2)):
        if(lst2[j]<lst1[i]):
            s.append(lst2[j])
            j=j+1
        else:
            s.append(lst1[i])
            i=i+1
            
    if(i==len(lst1)):
        s.extend(lst2[j:])
    else:
        s.extend(lst1[i:])
            
    return s


