
def verbing(s):
  if(len(s)>=3): 
    if s[-3:]=='ing':
        return s+'ly'
    else:
        return s+'ing'
  else:
    return s




def not_bad(s):
    x=s.find('not')
    y=s.find('bad')
    if(x>=0 and x<y)
      return s[:x]+'good'+s[y+3:]
    else
      return s


def front_back(a,b):
  x=len(a)
  y=len(b)
  p=x//2+x%2+1
  r=y//2+y%2+1
  s[]
  s=a[:p]+b[:r]+a[p:]+b[r:]
  return s

  
