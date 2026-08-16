def matran(m,n):
    return [[m*n for i in range(1,m+1)] for j in range(1,n+1)]

def tinhtrungbinh(*args):
    avg = sum(args)/len(args)
    return avg

def antoanchia(a,b):
    try:
        return a/b
    except ZeroDivisionError:
        return None

def max(**kwargs):
    maxx = next(iter(kwargs.items()))
    maxxx = maxx[1]
    ten = maxx[0]
    for key, value in kwargs.items():
        if value > maxxx:
            maxxx = value
            ten = key
    return ten