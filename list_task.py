def remove_adjacent(s):
    i=0
    while (i<len(s)):
        if(s[i]==s[i-1]):
            s.pop(i)
        i=i+1
            
            
    return s


def linear_merge(lst1, lst2):
    s=[]
    i=0
    j=0
    while(i<len(lst1) and j<len(lst2)):
         while (i<len(lst1) and lst1[i]<=lst2[j]):
            s.append(lst1[i])
            i=i+1
         while (j<len(lst2) and lst1[i]>=lst2[j]):
            s.append(lst2[j])
            j=j+1
    if(i==len(lst1)and j!=len(lst2)):
        for p in range(j,len(lst2)):
            s.append(lst2[p])
    if(i!=len(lst1)and j==len(lst2)):
        for p in range(i,len(lst1)):
            s.append(lst1[p])
            
    return s


