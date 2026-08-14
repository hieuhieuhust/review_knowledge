import pandas as pd

data = {
    "ten": ["an", "binh", "chi", "dung", "em"],
    "phongban": ["Sales", "IT", "Sales", "IT", "HR"],
    "tuoi": [23, 25, 22, 30, 28],
    "luong": [8000000, 12000000, 7500000, 15000000, 9000000]
}

df = pd.DataFrame(data)

def luonghon9cu(a):
    df = pd.DataFrame(a)
    b = df[df["luong"] > 9000000]
    return b["ten"].tolist()

def luontrungbinh(a):
    df = pd.DataFrame(a)
    b = df.groupby("phongban")["luong"].mean()
    return b

def them1cotmoi(a, b):
    df = pd.DataFrame(a)
    df[b] = df["luong"]*0.1
    return df