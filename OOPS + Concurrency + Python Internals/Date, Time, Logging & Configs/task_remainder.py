import datetime
import logging
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "taskHistory.log")
TASK_FILE = os.path.join(BASE_DIR, "tasks.json")
DATE_FORMAT = "%d-%m-%Y %H:%M"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

tasks = {}

def load_tasks():
    global tasks
    if not os.path.exists(TASK_FILE):
        return
    try:
        with open(TASK_FILE, "r") as f:
            tasks=json.load(f)
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Failed to load tasks: {e}")

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def create_task():
    print("--- Creating New Task ---")
    title = input("Heading: ")
    note = input("Note: ")
    start = input(f"Enter start time (format:{DATE_FORMAT}): ")
    end = input(f"Enter end time (format:{DATE_FORMAT}): ")

    try:
        start_dt = datetime.datetime.strptime(start, DATE_FORMAT)
        end_dt = datetime.datetime.strptime(end, DATE_FORMAT)
    except ValueError:
        print("Invalid date format")
        return
    
    if start_dt >= end_dt:
        print("Start time should be before End time")
        return


    overlaps = []

    for t_title, t in tasks.items():
        existing_start = datetime.datetime.strptime(t["start"], DATE_FORMAT)
        existing_end = datetime.datetime.strptime(t["end"], DATE_FORMAT)

        if start_dt < existing_end and end_dt > existing_start:
            overlaps.append(t_title)


    if len(overlaps)!=0:
        print(f" Warning: Overlaps with {', '.join(overlaps)}")
        logging.warning("Warning: Overlapping tasks")

        if input("Allow overlap (y/n): ").lower() != 'y':
            return  
    
    reminder = input("Enable daily reminder? (y/n): ").lower() == "y"
    
    tasks[title]={"notes":note, "start": start, "end":end, "daily reminder": reminder}
    
    save_tasks()
    logging.info(f"Created: {title}")
    print("Task created successfully.")


def delete_task():
    view_task_titles()
    title = input("\nEnter task title to delete: ").strip()

    if title not in tasks:
        print("Task not found.")
        return

    end_time = datetime.datetime.strptime(tasks[title]["end"], DATE_FORMAT)
    is_expired = end_time < datetime.datetime.now()
    
    if not is_expired:
        confirm = input(f"Task '{title}' is still active. Delete anyway? (y/n): ").lower()
        if confirm != 'y':
            return

    tasks.pop(title)
    save_tasks()
    logging.info(f"Deleted: {title}")
    print("Task removed.")

def modify_task():
    if len(tasks) == 0:
        print("No tasks available.")
        return

    view_task_titles()
    title = input("\nEnter task title to modify: ").strip()

    if title not in tasks:
        print("Task not found.")
        return

    task = tasks[title]

    print("\nPress Enter to keep existing values")

    new_note = input("Notes [" + task["notes"] + "]: ")
    if new_note != "":
        task["notes"] = new_note

    new_start = input("Start time [" + task["start"] + "]: ")
    if new_start != "":
        try:
            datetime.datetime.strptime(new_start, DATE_FORMAT)
            task["start"] = new_start
        except ValueError:
            print("Invalid start time format. Keeping old value.")

    new_end = input("End time [" + task["end"] + "]: ")
    if new_end != "":
        try:
            datetime.datetime.strptime(new_end, DATE_FORMAT)
            task["end"] = new_end
        except ValueError:
            print("Invalid end time format. Keeping old value.")

    start_dt = datetime.datetime.strptime(task["start"], DATE_FORMAT)
    end_dt = datetime.datetime.strptime(task["end"], DATE_FORMAT)

    if start_dt >= end_dt:
        print("Start time must be before end time. Changes cancelled.")
        return
    
    current_reminder = "y" if task["daily reminder"] else "n"
    reminder_input = input("Daily reminder (y/n) [" + current_reminder + "]: ").lower()

    if reminder_input == "y":
        task["daily reminder"] = True
    elif reminder_input == "n":
        task["daily reminder"] = False

    save_tasks()
    logging.info("Modified task: " + title)
    print("Task updated successfully.")


def view_full_tasks():
    print("Available tasks:")
    print(f"\n  {'TASK':<18} | {'STARTING TIME':<18} | {'ENDING TIME':<18} | {'DAILY REMAINDER':<10}")
    for i in tasks:
        print(f"- {tasks[i]['notes']:<18} | {tasks[i]['start']:<18} | {tasks[i]['end']:<18} | {tasks[i]['daily reminder']:<10}")

def view_task_titles():
    print("Available tasks:")
    for i in tasks:
        print(f"- {i}")


def maintain_task():
    now = datetime.datetime.now()
    to_delete = []

    for title, info in tasks.items():
        end_time = datetime.datetime.strptime(info["end"], DATE_FORMAT)

        if not info["daily reminder"] and end_time < now:
            to_delete.append(title)

    for title in to_delete:
        tasks.pop(title)
        logging.info(f"Auto-deleted expired task: {title}")

    if to_delete:
        save_tasks()

load_tasks()

while True:
    maintain_task()
    print()
    print("1. Create  2. Modify  3. Delete  4. View Detailed  5. View List  6. Exit")
    
    choice = input("\nChoice: ")

    match choice:
        case '1':
            create_task()
        case '2':
            modify_task()
        case '3':
            delete_task()
        case '4':
            view_full_tasks()
        case '5':
            view_task_titles()
        case '6':
            print("Exiting..")
            break
        case _ :
            print("Invalid selection.")