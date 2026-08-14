import numpy as np

list = [1, 2,3,4,5]

def inrashape(a):
    arr = np.array(a)
    shape = np.shape(arr)
    tong = np.sum(arr)
    return shape, tong

def tinhpheptinh(a):
    arr = np.array(a)
    return arr*3 +1 

list2x3 = np.random.randint(0,10, (2,3))

def incotthu2(a):
    arr = np.array(a)
    return arr[:, 1]
    
    