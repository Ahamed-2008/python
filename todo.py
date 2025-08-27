from os import name


class Task:
    def __init__(self, name, due_date, priority):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.completed = False

    def __str__(self):
        return f"{self.name} (Due: {self.due_date}, Priority: {self.priority})"

    def mark_completed(self):
        self.completed = True
        print(f"Task {self.name} has been completed. Congrats!")

    def edit_task(self, new_name, new_due_date, new_priority):
        self.name = name
        self.due_date = new_due_date
        self.priority = new_priority
        print(f"Task {self.name} has been edited.")

print("Welcome to the task manager:")
tasks = []
while True:
    if not tasks:
        print("You task list is empty. Add new tasks to get started")
        while True:
            name = input("Enter task name: ")
            due_date = input("Enter due date: ")
            priority = input("Enter priority: ")
            task = Task(name, due_date, priority)
            tasks.append(task)
            print(f"Task {name} has been added to the list.")
            if input("Do you want to add another task? (y/n): ") != "y":
                break
    else:
        print("Your current tasks are:")
        for task in tasks:
            print(task)
        if input("Do you want to add new tasks? (y/n): ") == "y":
            while True:
                name = input("Enter task name: ")
                due_date = input("Enter due date: ")
                priority = input("Enter the priority: ")
                task = Task(name, due_date, priority)
                tasks.append(task)
                print(f"Task {name} has been added to the list.")
                if input("Do you want to add another task? (y/n): ") != "y":
                    break
        else:
            inp = input("Wnat do you want to do: ")
            match inp:
                case "mark completed":
                    taskno = int(input("Enter task number: "))
                    tasks[taskno-1].mark_completed()
                    print(f"Congrats! You completed the task {tasks[taskno-1].name}")
                    tasks.pop(taskno-1)
                case "edit task":
                    taskno = int(input("Enter task number: "))
                    new_name = input("Enter the new name for the task: ")
                    new_due_date = input("Enter the new due date for the task: ")
                    new_priority = input("Enter the new priority for the task:")
                    tasks[taskno-1].edit_task(new_name, new_due_date, new_priority)
                case "view task":
                    taskno = int(input("Enter task number: "))
                    print(tasks[taskno-1])
                case "exit":
                    break
                case _:
                    print("Invalid input. Please try again.")
                    continue

