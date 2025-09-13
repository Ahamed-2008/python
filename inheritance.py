class UniversityMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

class Student(UniversityMember):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def display_info(self):
        super().display_info()
        print(f"Student ID: {self.student_id}")

class Teacher(UniversityMember):
    def __init__(self, name, age, emp_id):
        super().__init__(name, age)
        self.emp_id = emp_id
    def display_info(self):
        super().display_info()
        print(f"Employee id: {self.emp_id}")
    
s1 = Student("Dhanish", 17, 1)
t1 = Teacher("Vignesh", 45, 2)
s1.display_info()
t1.display_info()