import tkinter as tk
from tkinter.simpledialog import askfloat
from tkinter import Menu
from PIL import ImageGrab
import math


class PlansWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Создание плана помещения")
        self.geometry("800x600")

        # Полотно для рисования плана с полосами прокрутки
        scrollbar_v = tk.Scrollbar(self, orient="vertical")
        scrollbar_h = tk.Scrollbar(self, orient="horizontal")
        self.plan_canvas = tk.Canvas(self, bg="white",
                                     scrollregion=(0, 0, 2200, 1100))  # Большой холст 2200×1100 пикселей
        scrollbar_v.config(command=self.plan_canvas.yview)
        scrollbar_h.config(command=self.plan_canvas.xview)
        self.plan_canvas.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # Располагаем элементы на форме
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        self.plan_canvas.pack(fill="both", expand=True)

        # Панель кнопок внизу окна
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side="bottom", fill="x")

        # Кнопки
        perim_btn = tk.Button(buttons_frame, text="Периметр дома", command=self.draw_house_perimeter)
        wall_btn = tk.Button(buttons_frame, text="Добавить стену", command=self.add_wall)
        door_btn = tk.Button(buttons_frame, text="Добавить дверь", command=self.add_door)
        win_btn = tk.Button(buttons_frame, text="Добавить окно", command=self.add_window)
        scale_btn = tk.Button(buttons_frame, text="Масштабировать", command=self.scale_plan)
        save_btn = tk.Button(buttons_frame, text="Сохранить план", command=self.save_plan)
        open_btn = tk.Button(buttons_frame, text="Открыть план", command=self.open_plan)

        # Упаковка кнопок слева направо
        perim_btn.pack(side="left", padx=5)
        wall_btn.pack(side="left", padx=5)
        door_btn.pack(side="left", padx=5)
        win_btn.pack(side="left", padx=5)
        scale_btn.pack(side="left", padx=5)
        save_btn.pack(side="left", padx=5)
        open_btn.pack(side="left", padx=5)

        # Переменные для рисования
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.mode = ""

        # Привязка событий мыши
        self.plan_canvas.bind("<Button-1>", self.start_drawing)
        self.plan_canvas.bind("<B1-Motion>", self.drawing)
        self.plan_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def draw_house_perimeter(self):
        """Формирует наружный периметр дома по заданным размерам"""
        house_length = askfloat("Длина дома", "Введите длину дома в метрах:", initialvalue=7.05)
        house_width = askfloat("Ширина дома", "Введите ширину дома в метрах:", initialvalue=5.0)
        wall_thickness = askfloat("Толщина стен", "Введите толщину стен в метрах:", initialvalue=0.2)

        if house_length is None or house_width is None or wall_thickness is None:
            return

        # Переводим в пиксели (примерно 1 пиксель = 10 см)
        scale = 100  # 1 пиксель = 10 см
        outer_length_px = house_length * scale
        outer_width_px = house_width * scale
        inner_length_px = outer_length_px * 0.7  # Внутренняя длина (70%)
        inner_width_px = outer_width_px * 0.7  # Внутренняя ширина (70%)
        thickness_px = wall_thickness * scale

        # Формируем периметр
        perimeter_points = [
            (thickness_px, thickness_px, inner_length_px + thickness_px, thickness_px),  # Верхняя стена
            (inner_length_px + thickness_px, thickness_px, inner_length_px + thickness_px,
             inner_width_px + thickness_px),  # Правая стена
            (inner_length_px + thickness_px, inner_width_px + thickness_px, thickness_px,
             inner_width_px + thickness_px),  # Нижняя стена
            (thickness_px, inner_width_px + thickness_px, thickness_px, thickness_px)  # Левая стена
        ]

        # Отрисовка периметра
        for line in perimeter_points:
            self.plan_canvas.create_line(line, fill="gray", width=thickness_px)

        # Отображение размеров
        self.plan_canvas.create_text(thickness_px + inner_length_px / 2, thickness_px / 2,
                                     text=f"{outer_length_px / scale:.2f}m", fill="black")
        self.plan_canvas.create_text(thickness_px / 2, thickness_px + inner_width_px / 2,
                                     text=f"{outer_width_px / scale:.2f}m", fill="black")

    def add_wall(self):
        """Режим рисования стен"""
        self.mode = "add_wall"
        print("Режим рисования стен включен")

    def add_door(self):
        """Режим добавления дверей"""
        self.mode = "add_door"
        print("Режим добавления дверей включен")

    def add_window(self):
        """Режим добавления окон"""
        self.mode = "add_window"
        print("Режим добавления окон включен")

    def scale_plan(self):
        """Управление масштабом плана"""
        print("Масштабирование включено")

    def save_plan(self):
        """Сохранение текущего плана"""
        print("Сохранение плана выполнено")

    def open_plan(self):
        """Открытие существующего плана"""
        print("Открытие плана выполнено")

    def start_drawing(self, event):
        """Начало рисования фигуры"""
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = None

    def drawing(self, event):
        """Процесс рисования фигуры"""
        colors = {"wall": "#A9A9A9", "door": "#FFFFFF", "window": "#ADD8E6"}  # Серая стена, белая дверь, голубое окно
        current_color = colors.get(self.mode, "#000000")

        if self.mode == "wall":
            # Если указана длина стены, используем её
            if self.wall_length is not None:
                direction_vector = (event.x - self.start_x, event.y - self.start_y)
                vector_length = math.hypot(*direction_vector)
                normalized_direction = tuple(val / vector_length for val in direction_vector)
                final_point = (
                    self.start_x + normalized_direction[0] * self.wall_length * 100,
                    self.start_y + normalized_direction[1] * self.wall_length * 100
                )
                self.current_shape = self.plan_canvas.create_line(self.start_x, self.start_y, final_point[0],
                                                                  final_point[1], fill=current_color,
                                                                  width=int(self.wall_thickness * 100))
            else:
                # Без ограничения длины
                self.current_shape = self.plan_canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                                                  fill=current_color,
                                                                  width=int(self.wall_thickness * 100))
        else:
            # Рисуем дверь или окно
            self.current_shape = self.plan_canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10,
                                                              fill=current_color)

    def stop_drawing(self, event):
        """Завершение рисования фигуры"""
        if self.current_shape:
            self.plan_canvas.itemconfig(self.current_shape, tags=(self.mode,))
        self.current_shape = None


if __name__ == "__main__":
    root = tk.Tk()
    app = PlansWindow(master=root)
    app.mainloop()