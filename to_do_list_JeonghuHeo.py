from datetime import datetime

MAINTENANCE_SCHEDULE = {
    "Compact Car": [
        ("Engine Oil", "High", "Replace every 15,000 km or 1 year, whichever comes first"),
        ("Brake Pads", "Medium", "Check every 20,000 km or 2 years"),
        ("Tires", "Medium", "Replace every 50,000 km")
    ],
    "Sedan": [
        ("Engine Oil", "High", "Replace every 10,000 km or 1 year, whichever comes first"),
        ("Brake Pads", "Medium", "Check every 30,000 km or 2 years"),
        ("Tires", "Medium", "Replace every 60,000 km")
    ],
    "SUV": [
        ("Engine Oil", "High", "Replace every 7,500 km or 1 year, whichever comes first"),
        ("Brake Pads", "Medium", "Check every 25,000 km or 2 years"),
        ("Tires", "Medium", "Replace every 40,000 km")
    ]
}

class Recommendation:

    def __init__(self, maintenance_schedule):
        self.maintenance_schedule = maintenance_schedule
        self.current_year = datetime.now().year

    def get_car_info(self):

        print("\n--- Enter Car Information ---")
        try:
            car_type = input("Enter car type (Compact Car, Sedan, SUV): ").strip()
            if car_type not in self.maintenance_schedule:
                raise ValueError("Invalid car type entered.")

            year = int(input("Enter car year (e.g. 2021): ").strip())
            mileage = int(input("Enter car mileage (e.g. 30000): ").strip())
            return car_type, year, mileage

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
            return self.get_car_info()

    def get_recommended_tasks(self, car_type, year, mileage):

        tasks = []
        for item, priority, description in self.maintenance_schedule.get(car_type, []):
            car_age = self.current_year - year
            if car_age > 5 or mileage > 100000:
                description += " - Requires more frequent maintenance due to car age/mileage"
            tasks.append((item, priority, description))
        return tasks

class Task:
    def __init__(self, item, priority, description="", completed=False):
        self.item = item
        self.priority = priority
        self.description = description
        self.completed = completed

    def __repr__(self):
        return (f"Task(item='{self.item}', priority='{self.priority}',"
                f" description='{self.description}', completed={self.completed})")

class TaskManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tasks = self.read_tasks_from_file()
        self.recommendation= Recommendation(MAINTENANCE_SCHEDULE)
        self.car_info = None
    
    def initialize_car_info(self):
        if not self.car_info:
            print("\n--- Initializing Car Information ---")
            self.car_info = self.recommendation.get_car_info()
            print("Car information saved.")
        else:
            print("Car information is already initialized")

    def show_all_tasks(self):
        print("\n--- All Tasks ---")
        if not self.tasks:
            print("No tasks available.")
            return
        for idx, task in enumerate(self.tasks, start=1):
            status = "Done" if task.completed else "Pending"
            print(f"{idx}. {task.item} (Priority: {task.priority}) - [{status}]")
            if task.description:
                print(f"   Description: {task.description}")

    def add_task(self):
        self.initialize_car_info()
        car_type, year, mileage = self.car_info
        recommended_tasks = self.recommendation.get_recommended_tasks(car_type, year, mileage)

        if recommended_tasks:
            print("\n--- Recommended Maintenance Tasks ---")
            for idx, (item, priority, description) in enumerate(recommended_tasks, 1):
                print(f"{idx}. {item} - Priority: {priority}, {description}")
            print("\nEnter '0' to skip these and add a custom task.")

            while True:
                try:
                    task_number = int(input("Select the task number to add or 0 to skip: ").strip())
                    if task_number == 0:
                        break
                    elif 1 <= task_number <= len(recommended_tasks):
                        item, priority, description = recommended_tasks[task_number - 1]
                        self.tasks.append(Task(item, priority, description))
                        print(f"Task '{item}' added successfully.")
                        return
                    else:
                        print("Invalid number. Please select a valid option.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

        print("\n--- Enter Custom Task Details ---")
        item = input("Enter the item name: ")
        priority = input("Enter the priority level (High, Medium, Low): ")
        description = input("Enter the description (optional): ")
        self.tasks.append(Task(item, priority, description))
        print(f"Task '{item}' added successfully.")

    def complete_task(self):

        self.show_all_tasks()
        try:
            index = int(input("Enter the task number to mark as completed: ").strip()) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index].completed = True
                print(f"Task '{self.tasks[index].item}' marked as completed.")
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def remove_task(self):

        self.show_all_tasks()
        try:
            index = int(input("Enter the task number to remove: ").strip()) - 1
            if 0 <= index < len(self.tasks):
                removed_task = self.tasks.pop(index)
                print(f"Task '{removed_task.item}' removed successfully.")
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def save_tasks_to_file(self):

        with open(self.file_name, "w") as file:
            for task in self.tasks:
                file.write(f"Item: {task.item}\n")
                file.write(f"Priority: {task.priority}\n")
                if task.description.strip():
                    file.write(f"Description: {task.description}\n")
                file.write(f"Completed: {str(task.completed)}\n")
                file.write("\n")
        print(f"Tasks saved to '{self.file_name}' successfully.")

    def read_tasks_from_file(self):

        tasks = []
        try:
            with open(self.file_name, "r") as file:
                item, priority, description, completed_str = "", "", "", ""
                for line in file:
                    line = line.strip()
                    if line.startswith("Item:"):
                        if item:
                            completed_bool = (completed_str.lower() == "true")
                            tasks.append(Task(item, priority, description, completed_bool))
                        item = line.replace("Item:", "").strip()
                        priority, description, completed_str = "", "", ""
                    elif line.startswith("Priority:"):
                        priority = line.replace("Priority:", "").strip()
                    elif line.startswith("Description:"):
                        description = line.replace("Description:", "").strip()
                    elif line.startswith("Completed:"):
                        completed_str = line.replace("Completed:", "").strip()
                if item:
                    completed_bool = (completed_str.lower() == "true")
                    tasks.append(Task(item, priority, description, completed_bool))
        except FileNotFoundError:
            print(f"File '{self.file_name}' not found. Starting with an empty task list.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
        return tasks

def main():
    manager = TaskManager("tasks.txt")

    while True:
        try:
            print("\n--- Menu ---")
            print("1. Show all tasks")
            print("2. Add a new task")
            print("3. Complete tasks")
            print("4. Remove tasks")
            print("5. Save tasks to file")
            print("6. Exit")

            choice = int(input("Enter your choice: ").strip())

            if choice == 1:
                manager.show_all_tasks()

            elif choice == 2:
                manager.add_task()

            elif choice == 3:
                manager.complete_task()

            elif choice == 4:
                manager.remove_task()

            elif choice == 5:
                manager.save_tasks_to_file()

            elif choice == 6:
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
