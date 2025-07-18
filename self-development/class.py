class Task:
    def __init__(self, title):
        self.title = title
        self.done = False

    def mark_done(self):
        self.done = True

    def __str__(self):
        status = "✅ Done" if self.done else "❌ Not done"
        return f"{self.title} — {status}"
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_task_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()

    def show_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i}. {task}")
if __name__ == "__main__":
    manager = TaskManager()

    while True:
        print("\n1. Add Task")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Remove Task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            manager.add_task(title)

        elif choice == '2':
            manager.show_tasks()

        elif choice == '3':
            index = int(input("Enter task index to mark as done: "))
            manager.mark_task_done(index)

        elif choice == '4':
            index = int(input("Enter task index to remove: "))
            manager.remove_task(index)

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")
