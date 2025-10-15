import tkinter as tk
from tkinter.colorchooser import askcolor


class EngineeringSystemsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Инженерные системы")
        self.geometry("800x600")

        # Канва для рисования инженерных систем
        self.systems_canvas = tk.Canvas(self, bg="lightgrey")
        self.systems_canvas.pack(fill="both", expand=True)

        # Меню выбора режимов
        modes_frame = tk.Frame(self)
        electric_btn = tk.Button(modes_frame, text="Электрические устройства",
                                 command=lambda: self.set_mode("electric"))
        water_btn = tk.Button(modes_frame, text="Водопровод", command=lambda: self.set_mode("water"))
        ventilation_btn = tk.Button(modes_frame, text="Вентиляция", command=lambda: self.set_mode("ventilation"))
        electric_btn.pack(side="left", padx=5)
        water_btn.pack(side="left", padx=5)
        ventilation_btn.pack(side="left", padx=5)
        modes_frame.pack(side="top", pady=10)

        # Трекинг выбранного режима
        self.mode = "none"

        # Назначение методов рисования
        self.systems_canvas.bind("<Button-1>", self.start_drawing)
        self.systems_canvas.bind("<B1-Motion>", self.drawing)
        self.systems_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def set_mode(self, new_mode):
        """Устанавливает текущий режим рисования инженерной системы"""
        self.mode = new_mode
        print(f"Установлен режим: {new_mode}")

    def start_drawing(self, event):
        """Начинаем рисование инженерной системы"""
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = None

    def drawing(self, event):
        """Сам процесс рисования системы"""
        if self.mode == "electric":
            color = "#ffa500"  # Электрические провода - оранжевый
        elif self.mode == "water":
            color = "#0000ff"  # Водопровод - синий
        elif self.mode == "ventilation":
            color = "#808080"  # Вентиляция - серый
        else:
            color = "#000000"  # Чёрный цвет по умолчанию

        if self.current_shape:
            self.systems_canvas.delete(self.current_shape)
        self.current_shape = self.systems_canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=color,
                                                             width=3)

    def stop_drawing(self, event):
        """Завершаем рисование инженерной системы"""
        if self.current_shape:
            self.systems_canvas.itemconfig(self.current_shape, tags=(self.mode,))
        self.current_shape = None


if __name__ == "__main__":
    root = tk.Tk()
    app = EngineeringSystemsWindow(master=root)
    app.mainloop()