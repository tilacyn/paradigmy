
def verbing(s):
  if(len(s)>=3): 
    if s[-3:]=='ing':
        s=s+'ly'
    else:
        s=s+'ing'
    return s



def not_bad(s):
    boo=foo=0
    for i in range (0, len(s)-3):
        if(s[i:i+3]=='not' and not boo):
            p=i
            boo=1
        if(s[i:i+3]=='bad' and boo):
            d=i
            foo=1
            break;
    if(foo):
        s=s[:p]+'good'+s[(d+3):]
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

  
