import json 
import os 

def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(tasks):
    title = input("Enter task title: ")
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)

def show_tasks(tasks):
    for i, task in enumerate(tasks):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} — {status}")

def mark_done(tasks):
    index = int(input("Enter task index to mark as done: "))
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)

def delete_task(tasks):
    index = int(input("Enter task index to delete: "))
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)


if __name__ == "__main__":
    tasks = load_tasks()

    while True:
        print("\n1. Add Task")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose: ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            show_tasks(tasks)
        elif choice == '3':
            mark_done(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print("Invalid choice!")
       

