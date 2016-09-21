
def verbing(s):
  if(len(s)>=3): 
    if s[-3:]=='ing':
        return s+'ly'
    else:
        return s+'ing'




def not_bad(s):
    x=s.find('not')
    y=s.find('bad')
    if(x>=0 and y>=0 and x<y)
      return s[:x]+'good'+s[y+3:]
    else
      return s


def front_back(a,b):
  x=len(a)
  y=len(b)
  if(x%2==0):
    s=a[0:(x//2)]
    if(len(b)%2==0):
      s=s+b[0:(y//2)]
      s=s+a[(x//2):x]
      s=s+b[(y//2):y]
    else:
      s=s+b[0:(y//2)+1]
      s=s+a[(x//2):x]
      s=s+b[(y//2)+1:y]
  else:
    s=a[0:(x//2)+1]
    if(len(b)%2==0):
      s=s+b[0:(y//2)]
      s=s+a[(x//2)+1:x]
      s=s+b[(y//2):y]
    else:
      s=s+b[0:(y//2)+1]
      s=s+a[(x//2)+1:x]
      s=s+b[(y//2)+1:y]
    
  return s

  
