import pandas as pd 

nhan_vien = pd.DataFrame({
    "ten": ["An", "Binh", "Chi", "Dung", "Em"],
    "phong_ban": ["Sales", "IT", "Sales", "IT", "HR"],
    "luong": [8000000, 12000000, None, 15000000, 9000000]   # Chi bị thiếu lương
})

phong_ban_info = pd.DataFrame({
    "phong_ban": ["Sales", "IT", "HR"],
    "truong_phong": ["Nam", "Lan", "Hoa"]
})

def ghepbang(a,b):
    nv_pbinfor = nhan_vien.merge(phong_ban_info, on= "phongban")
    return nv_pbinfor[["ten", "phongban", "luong", "truongphong"]]

def diengiatrithieu(a):
    return(a["luong"].fillna(a["luong"].mean()))
    
def tinhluongtrungbinh(a):
    b = a.pivot_table(values = "luong", index ="phongban", aggfunc= "mean")
    return b