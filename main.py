import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from plans import PlansWindow
from engineering_systems import EngineeringSystemsWindow


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Планировщик помещений")
        self.geometry("800x600")

        # Панель для отображения плана
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Кнопка "Создать план"
        create_plan_btn = ttk.Button(self, text="Создать план", command=self.show_plans_window)
        create_plan_btn.pack(pady=20)

        # Кнопка "Инженерные системы"
        engineering_btn = ttk.Button(self, text="Инженерные системы", command=self.show_engineering_systems)
        engineering_btn.pack(pady=20)

        # Кнопка "Сохранить в PDF"
        save_pdf_btn = ttk.Button(self, text="Сохранить в PDF", command=self.save_to_pdf)
        save_pdf_btn.pack(pady=20)

        # Статусная строка
        self.status_label = ttk.Label(self, text="", foreground="green")
        self.status_label.pack(side="bottom", pady=10)

    def update_plan_view(self, path):
        """Обновляет представление плана в главном окне"""
        if os.path.exists(path):
            img = Image.open(path)
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        else:
            self.canvas.delete("all")
            self.canvas.configure(bg="white")

    def show_plans_window(self):
        """Отображает окно создания плана помещения"""
        plans_window = PlansWindow(self)
        plans_window.focus_set()
        plans_window.grab_set()

    def show_engineering_systems(self):
        """Отображает окно инженерных систем"""
        engineering_window = EngineeringSystemsWindow(self)
        engineering_window.focus_set()
        engineering_window.grab_set()

    def save_to_pdf(self):
        """Заглушка для будущего метода сохранения в PDF"""
        print("Функция сохранения в PDF пока не реализована.")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()