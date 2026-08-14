import math

def timsole(n):
    if n%2 == 1:
        return "lẻ"
    else:
        return "chẵn"

def tong1toin(n):
    tong = 0
    for i in range(1,n+1):
        tong = tong + i
    return tong

def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result

def chuoipalindrome(s):
    reverse = ""
    for char in s:
        reverse = char + reverse
    return s == reverse

def soluongtutrongchuoi(s):
    d = {}
    for char in s:
        if char in d:
            d[char] += 1
        else:
            d[char] = 1 
    return d

def soluongtutrongchuoi2(s):
    d = {}
    for char in s:
        d[char] = d.get(char,0) + 1
    return d
                