#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk, messagebox
from classes import Task, TaskManager

class TaskManagerApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.setup_ui()

    def setup_ui(self):
        # Поля ввода
        tk.Label(self.root, text="Название").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Описание").grid(row=1, column=0)
        self.desc_text = tk.Text(self.root, height=3, width=30)
        self.desc_text.grid(row=1, column=1)

        tk.Label(self.root, text="Срок выполнения (ГГГГ-ММ-ДД)").grid(row=2, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1)

        # Кнопки
        tk.Button(self.root, text="Добавить", command=self.add_task).grid(row=3, column=0)
        tk.Button(self.root, text="Удалить", command=self.delete_task).grid(row=3, column=1)
        tk.Button(self.root, text="Сохранить в TXT", command=self.save_all_to_txt).grid(row=3, column=2)

        # Список задач
        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.grid(row=4, column=0, columnspan=2)
        self.update_listbox()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get()
        if title and description and due_date:
            task = Task(title, description, due_date)
            self.manager.add_task(task)
            self.update_listbox()
            self.clear_inputs()
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            self.manager.delete_task(selected[0])
            self.update_listbox()
     
    def save_all_to_txt(self):
         from tkinter import filedialog, messagebox
         path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text files", "*.txt")],
                                        title="Сохранить задачи в TXT")
         if not path:
            return
         try:
             with open(path, "w", encoding="utf-8") as f:
                 for task in self.manager.tasks:
                     f.write(f"Название: {task.title}\n")
                     f.write(f"Описание: {task.description}\n")
                     f.write(f"Срок выполнения: {task.due_date}\n")
                     f.write("-" * 30 + "\n")
             messagebox.showinfo("Сохранение", f"Задачи сохранены в {path}")
         except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
 
    def update_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, f"{task.title} (до {task.due_date})")

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

