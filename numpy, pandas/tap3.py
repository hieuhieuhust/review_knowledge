def is_palindrome_v2(s):
    left = 0
    right = len(s) -1 
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -=1
    return True    
        
        
def sum2target(s, target):
    left = 0
    right = len(s) -1 
    while left < right:
        if s[left] + s[right] == target:
            return [left, right]
        elif s[left] + s[right] < target:
            left = left + 1
        elif s[left] + s[right] > target:
            right = right -1 
    return []

import numpy as np

def max_sum_subarrray(s,a):
    arr = np.array(s)
    summ = sum(arr[0:a]) # [0] + [1] +...+[a-1]
    for i in range(len(s)-1-a):
        if sum(arr[i: i+ (a)] < sum(arr[i+1: i+1 +(a)])):
            summ = sum(arr[i+1: i+1 + (a)])
    return summ