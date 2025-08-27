class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def move(self):
        print("Move!")

class Car(Vehicle):
    def move(self):
        print("Drive!")

class Boat(Vehicle):
    def move(self):
        print("Sail!")

class Plane(Vehicle):
    def move(self):
        print("Fly!")
        
car1 = Car("Toyota", "Camry")
boat1 = Boat("Lambhorgini", "Yacht 63")
plane1 = Plane("Boeing", "747")

car1.move()
boat1.move()
plane1.move()