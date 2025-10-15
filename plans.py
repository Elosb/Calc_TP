import tkinter as tk
from PIL import ImageGrab
import math


class PlansWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Создание плана помещения")
        self.geometry("800x600")

        # Переменная для отслеживания режима рисования
        self.mode = "wall"

        # Масштаб (начальный 1 пиксель = 1см)
        self.scale = 1.0

        # Полотно для рисования плана
        self.plan_canvas = tk.Canvas(self, bg="white")
        self.plan_canvas.pack(fill="both", expand=True)

        # Установка сетки координат
        self.setup_grid()

        # Меню выбора режимов
        modes_frame = tk.Frame(self)
        wall_btn = tk.Button(modes_frame, text="Добавить стену", command=lambda: self.set_mode("wall"))
        door_btn = tk.Button(modes_frame, text="Добавить дверь", command=lambda: self.set_mode("door"))
        window_btn = tk.Button(modes_frame, text="Добавить окно", command=lambda: self.set_mode("window"))
        zoom_in_btn = tk.Button(modes_frame, text="+", command=self.zoom_in)
        zoom_out_btn = tk.Button(modes_frame, text="-", command=self.zoom_out)
        wall_btn.pack(side="left", padx=5)
        door_btn.pack(side="left", padx=5)
        window_btn.pack(side="left", padx=5)
        zoom_in_btn.pack(side="left", padx=5)
        zoom_out_btn.pack(side="left", padx=5)
        modes_frame.pack(side="top", pady=10)

        # Кнопка "Сохранить"
        save_btn = tk.Button(self, text="Сохранить", command=self.save_plan)
        save_btn.pack(side="bottom", pady=10)

        # Переменные для рисования
        self.start_x = None
        self.start_y = None
        self.current_shape = None

        # Привязка событий мыши
        self.plan_canvas.bind("<Button-1>", self.start_drawing)
        self.plan_canvas.bind("<B1-Motion>", self.drawing)
        self.plan_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def setup_grid(self):
        """Отрисовка сетки координат"""
        canvas_width = int(self.plan_canvas['width'])
        canvas_height = int(self.plan_canvas['height'])
        grid_step = 10  # Шаг сетки в пикселях (соответствует 10 см)

        for i in range(grid_step, canvas_width, grid_step):
            self.plan_canvas.create_line(i, 0, i, canvas_height, dash=(1, 5), fill="#ccc")

        for j in range(grid_step, canvas_height, grid_step):
            self.plan_canvas.create_line(0, j, canvas_width, j, dash=(1, 5), fill="#ccc")

    def set_mode(self, new_mode):
        """Устанавливает текущий режим рисования"""
        self.mode = new_mode
        print(f"Установлен режим: {new_mode}")

    def start_drawing(self, event):
        """Начало рисования фигуры"""
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = None

    def drawing(self, event):
        """Процесс рисования фигуры"""
        colors = {"wall": "#A9A9A9", "door": "#FFFFFF", "window": "#ADD8E6"}  # Серая стена, белая дверь, голубое окно
        current_color = colors.get(self.mode, "#000000")

        if self.current_shape:
            self.plan_canvas.delete(self.current_shape)
        self.current_shape = self.plan_canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="",
                                                               fill=current_color)

    def stop_drawing(self, event):
        """Завершение рисования фигуры"""
        if self.current_shape:
            # Добавляем размеры стены (при условии, что стена нарисована горизонтально или вертикально)
            if abs(event.x - self.start_x) >= abs(event.y - self.start_y):
                wall_length = round(abs(event.x - self.start_x) / self.scale)
                position = ((event.x + self.start_x) / 2, event.y)
            else:
                wall_length = round(abs(event.y - self.start_y) / self.scale)
                position = (event.x, (event.y + self.start_y) / 2)

            # Выводим надпись с размером стены
            self.plan_canvas.create_text(position, text=f"{wall_length} см", fill="black")
            self.plan_canvas.itemconfig(self.current_shape, tags=(self.mode,))
        self.current_shape = None

    def save_plan(self):
        """Сохраняет текущий план в изображение и уведомляет главное окно"""
        try:
            # Получаем координаты и область окна
            x = self.winfo_rootx() + self.plan_canvas.winfo_x()
            y = self.winfo_rooty() + self.plan_canvas.winfo_y()
            x1 = x + self.plan_canvas.winfo_width()
            y1 = y + self.plan_canvas.winfo_height()

            # Захватываем область полотна и сохраняем как изображение
            screenshot = ImageGrab.grab(bbox=(x, y, x1, y1))
            temp_file = "current_plan.png"
            screenshot.save(temp_file)

            # Отправляем путь в главное окно
            self.master.update_plan_view(temp_file)
        except Exception as e:
            print(f"Ошибка при сохранении плана: {e}")

    def zoom_in(self):
        """Увеличивает масштаб"""
        self.scale *= 1.1
        self.redraw_all()

    def zoom_out(self):
        """Уменьшает масштаб"""
        self.scale /= 1.1
        self.redraw_all()

    def redraw_all(self):
        """Перерисовывает всю сцену с новым масштабом"""
        self.plan_canvas.delete("all")
        self.setup_grid()
        # Тут надо бы восстановить предыдущие рисунки (стены, окна, двери) с учетом масштаба
        # ...


if __name__ == "__main__":
    root = tk.Tk()
    app = PlansWindow(master=root)
    app.mainloop()