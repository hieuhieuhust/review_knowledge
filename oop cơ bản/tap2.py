def find_max(s):
    max = s[0]
    for i in range(len(s)):
        if max < s[i]:
            max = s[i]
    return max

def filter_even(s):
    a = []
    for i in range(len(s)):
        if s[i]%2 == 0:
            a.append(s[i])
    return a

def remove_duplicates(numbers):
    a = []
    for i in range(len(numbers)):
        if numbers[i] not in a:
            a.append(numbers[i])
    return a

def merge_to_dict(a,b):
    d = {}
    for i in range(len(a)):
        d[a[i]] = b[i]
    return d

def two_sum(numbers, target):
    capindex = {}
    for i in range(len(numbers)):
        soconlai = target - numbers[i]
        if soconlai in capindex:
            return [numbers[i], soconlai]
        capindex[numbers[i]] = i
    return []