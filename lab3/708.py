class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance        
    def deposit(self, dep):
        self.balance += dep
    def withdraw(self, wit):
        if wit > self.balance:
            return ("Insufficient Funds")
        else:
            self.balance  -= wit
            return self.balance

balance, withdraw = map(int, input().split())

c = Account("Zangar", balance)
print(c.withdraw(withdraw))