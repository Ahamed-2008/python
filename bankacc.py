class Bank:
    def __init__(self, name, accountnumber, balance):
        self.name = name
        self.accountnumber = accountnumber
        self.balance = balance
    
    def __str__(self):
        return f"{self.name} has the bank account {self.accountnumber} with a balance of {self.balance}"

    def add_money(self, amount):
        self.balance += amount
        print(f"You have successfully deposited rs {amount}")
        print(f"Your new balance is rs {self.balance}")
    
    def withdraw_money(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"You have successfully withdrawn rs {amount}")
            print(f"Your new balance is rs {self.balance}")
        else:
            print("Insufficient funds")



acc1 = Bank("Ahamed", "123456789", 10000)
while True:
    print(acc1)
    inp = input("Do you want to add or withdraw money? ")
    if inp == "add":
        amount = int(input("Enter the amount you want to add: "))
        acc1.add_money(amount)  
    else:
        amount = int(input("Enter the amount you want to withdraw: "))
        acc1.withdraw_money(amount)