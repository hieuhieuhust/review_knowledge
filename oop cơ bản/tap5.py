import math

class BankAccount:
    # khởi tạo hàm
    def __init__(self, balance = 0):
        self.__balance = balance
    
    def deposit(self, amount):
        self.__balance = self.__balance + amount
        return self.__balance
    
    def withdraw(self, amount):

        if amount > self.__balance:
            return "không đủ số lượng"
        else:
            self.__balance -= amount
            return self.__balance
        
    def check_balance(self):
        return f"số tiền của bạn còn lại là {self.__balance}"
    
    
class circle:
    def __init__(self, bankinh, pi = 3.14):
        self.pi = pi
        self.bankinh = bankinh
    
    def area(self):
        return self.pi * self.bankinh**2
    
class square:
    def __init__(self, canh):
        self.canh = canh
        
    def area(self):
        return self.canh ** 2
    
class rectangle:
    def __init__(self, dai, rong, goc):
        self.dai = dai
        self.rong = rong
        self.goc = goc
        
    def area(self):
        return self.dai * self.rong * math.sin(self.goc) /2

cachinh = [circle(4), rectangle(5, 6, 60), square(5)]
for hinh in cachinh:
    print(f"diện tích hình {hinh.area()}")