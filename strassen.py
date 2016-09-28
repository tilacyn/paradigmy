import numpy as np, math
def st2(n):
    p=2;
    while(p<n):
        p=p*2
    return p
def rec(a,b):
    w=math.sqrt(a.size)
    r=w//2
    if(w==2):
        return np.dot(a,b)
    else:
        a11=a[:r,:r]
        a12=a[:r,r:]
        a21=a[r:,:r]
        a22=a[r:,r:]
        b11=a[:r,:r]
        b11=b[:r,:r]
        b12=b[:r,r:]
        b21=b[r:,:r]
        b22=b[r:,r:]        
        c=np.zeros([w,w],int)
        p1=rec(a11+a22,b11+b22)
        p2=rec(a21+a22,b11)
        p3=rec(a11,b12-b22)
        p4=rec(a22,b21-b11)
        p5=rec(a11+a12,b22)
        p6=rec(a21-a11,b11+b12)
        p7=rec(a12-a22,b21+b22)
        c11=p1+p4-p5+p7
        c12=p3+p5
        c21=p2+p4
        c22=p1-p2+p3+p6
        c=np.vstack((np.hstack((c11,c12)),np.hstack((c21,c22))))
        return c[:n,:n]
n=int(input())
b=np.zeros([st2(n),st2(n)],int)
a=np.zeros([st2(n),st2(n)],int)
A=[]
for i in range(n):
     A.append(list(map(int, input().split())))
a[:n,:n]=A
B=[]
for i in range(n):
     B.append(list(map(int, input().split())))
b[:n,:n]=B
    
for i in rec(a,b):
        print (*i)

