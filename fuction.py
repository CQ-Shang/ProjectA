def f():
    x=int(input())
    if x<0:
        f=-1
    elif x==0:
        f=0
    else:
        f=2*x
    return f
if __name__=='__main__':
    f()