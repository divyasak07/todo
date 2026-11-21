
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "tasks.json"

# Load saved tasks
def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []

# Save tasks
def save_tasks():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        messagebox.showerror("Error", "Unable to save tasks.")

# Update task statistics
def update_stats():
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed

    stats_label.config(
        text=f"Total: {total}  |  Completed: {completed}  |  Pending: {pending}"
    )

# Display tasks
def refresh_tasks():
    task_list.delete(0, tk.END)

    for index, task in enumerate(tasks):
        status = "✓" if task["completed"] else "○"
        text = (
            f"{status}  {task['title']}  |  "
            f"{task['priority']}  |  Due: {task['due_date']}"
        )

        task_list.insert(tk.END, text)

        if task["completed"]:
            task_list.itemconfig(index, fg="gray")
        elif task["priority"] == "High":
            task_list.itemconfig(index, fg="#ff6b6b")
        elif task["priority"] == "Medium":
            task_list.itemconfig(index, fg="#f0c674")
        else:
            task_list.itemconfig(index, fg="#8bd5ca")

    update_stats()

# Add task
def add_task():
    title = task_entry.get().strip()
    due_date = date_entry.get().strip()
    priority = priority_box.get()

    if not title:
        messagebox.showwarning("Missing Task", "Enter a task name.")
        return

    if not due_date:
        due_date = "Not set"

    task = {
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

# Mark selected task complete
def complete_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showwarning("Selection", "Select a task first.")
        return

    index = selection[0]
    tasks[index]["completed"] = not tasks[index]["completed"]

    save_tasks()
    refresh_tasks()

# Delete selected task
def delete_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showwarning("Selection", "Select a task first.")
        return

    index = selection[0]

    if messagebox.askyesno("Confirm", "Delete this task?"):
        tasks.pop(index)
        save_tasks()
        refresh_tasks()

# Clear completed tasks
def clear_completed():
    global tasks

    tasks = [task for task in tasks if not task["completed"]]
    save_tasks()
    refresh_tasks()

# Main window
root = tk.Tk()
root.title("Smart To-Do List")
root.geometry("700x550")
root.configure(bg="#1a011f")
root.resizable(False, False)

# Title
title_label = tk.Label(
    root,
    text="SMART TO-DO LIST",
    font=("Arial", 22, "bold"),
    bg="#1e293b",
    fg="white"
)
title_label.pack(pady=20)

# Input frame
input_frame = tk.Frame(root, bg="#200229")
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Task:",
    bg="#1e293b",
    fg="white",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5, pady=5)

task_entry = tk.Entry(input_frame, width=25, font=("Arial", 11))
task_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Due Date:",
    bg="#1e293b",
    fg="white",
    font=("Arial", 11)
).grid(row=0, column=2, padx=5, pady=5)

date_entry = tk.Entry(input_frame, width=15, font=("Arial", 11))
date_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Priority:",
    bg="#1e293b",
    fg="white",
    font=("Arial", 11)
).grid(row=1, column=0, padx=5, pady=5)

priority_box = ttk.Combobox(
    input_frame,
    values=["High", "Medium", "Low"],
    width=22,
    state="readonly"
)
priority_box.grid(row=1, column=1, padx=5, pady=5)
priority_box.set("Medium")

# Add button
add_button = tk.Button(
    root,
    text="Add Task",
    command=add_task,
    bg="#38bdf8",
    fg="black",
    font=("Arial", 11, "bold"),
    padx=15
)
add_button.pack(pady=10)

# Task list
task_list = tk.Listbox(
    root,
    width=75,
    height=15,
    font=("Consolas", 10),
    bg="#0f172a",
    fg="white",
    selectbackground="#475569",
    borderwidth=0
)
task_list.pack(pady=15)

# Buttons frame
button_frame = tk.Frame(root, bg="#1e293b")
button_frame.pack(pady=5)

tk.Button(
    button_frame,
    text="Complete / Undo",
    command=complete_task,
    bg="#86efac",
    padx=10
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Delete Task",
    command=delete_task,
    bg="#fca5a5",
    padx=10
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Clear Completed",
    command=clear_completed,
    bg="#fcd34d",
    padx=10
).grid(row=0, column=2, padx=5)

# Statistics
stats_label = tk.Label(
    root,
    text="",
    font=("Arial", 12, "bold"),
    bg="#1e293b",
    fg="white"
)
stats_label.pack(pady=15)

# Initialize
tasks = load_tasks()
refresh_tasks()

root.mainloop()
