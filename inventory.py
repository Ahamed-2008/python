class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def restock(self, quantity):
        self.quantity += quantity

    def sell(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
        else:
            print("Not enough quantity available")
    def changeprice(self, price):
        self.price = price

    def __str__(self):
        return f"{self.name} , Price: {self.price} , Quantity: {self.quantity}"


p1 = Product("Chocolate", 100, 100000)
print(p1)
inp = input("Do you want to sell or restock the product: ")
if inp == "sell":
    quantity = int(input("Enter the quantity: "))
    p1.sell(quantity)
    print("Sold")
    print(p1)
else:
    quantity = int(input("Enter the quantity: "))
    p1.restock(quantity)
    print("Restocked")
    print(p1)
