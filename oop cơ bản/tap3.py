class animal:
    # hàm khởi tạo
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    # xây dựng phương thức
    def introduce(self):
        return "tôi tên là %s, tôi %d tuổi" % (self.name, self.age)
        
class Dog(animal):
    def __init__(self, name, age):
        super().__init__(name, age)
        
    def bark(self):
        return "%s: gâu gâu!" % (self.name)
        
class BankAccount:
    # hàm khởi tạo
    def __init__(self, balance=0):
        self.balance = balance
        
    # xây dựng phương thức
    def deposit(self, amount):
        self.balance = self.balance + amount
        
    def withdraw(self, amount):
        if self.balance < amount:
            return "số dư của bạn không đủ"
        else:
            self.balance = self.balance - amount
            
    def check_balance(self):
        return self.balance
         
