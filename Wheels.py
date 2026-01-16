import tkinter as tk
import random
import math

# Данные
items = [
    ("Никита", 40),
    ("Арсений", 20),
    ("Максон", 15),
    ("Костя", 10),
    ("Валик", 5),
    ("Лаврик", 5),
    ("Русик", 3),
    ("АЙФОН XL", 2),
]

names = [i[0] for i in items]
weights = [i[1] for i in items]

# Окно
root = tk.Tk()
root.title("Колесо фортуны")
root.geometry("400x550")

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(pady=20)

center = 150
radius = 120
angle_step = 360 / len(names)
current_angle = 0

# Стрелка
canvas.create_polygon(
    center - 10, 10,
    center + 10, 10,
    center, 30,
    fill="purple"
)

# Колесо (НЕНАВИЖУ ЕГО)
def draw_wheel(angle):
    canvas.delete("wheel")

    for i, name in enumerate(names):
        start = angle + i * angle_step
        canvas.create_arc(
            center - radius,
            center - radius,
            center + radius,
            center + radius,
            start=start,
            extent=angle_step,
        )

        text_angle = math.radians(start + angle_step / 2)
        x = center + math.cos(text_angle) * 80
        y = center - math.sin(text_angle) * 80

        canvas.create_text(
            x, y,
            text=name,
            font=("Arial", 10),
            tags="wheel"
        )

draw_wheel(current_angle)

# Результат
result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

def spin():
    global current_angle

    # Выбираем победителя по шансам
    winner = random.choices(names, weights=weights, k=1)[0]
    winner_index = names.index(winner)
    
    # Стрелка смотрит вверх
    ARROW_ANGE = 90

    # Поворачиваем колесо под стрелку
    winner_center = winner_index * angle_step + angle_step / 2

    # Перерисовка колеса
    draw_wheel(current_angle)
    
    #Показываем результат
    result_label.config(text=f"Выпало: {winner}")

# Кнопка
btn = tk.Button(root, text="Крутить", font=("Arial", 14), command=spin)
btn.pack(pady=10)

# Нижние  призы
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

for i, name in enumerate(names):
    lbl = tk.Label(
        bottom_frame,
        text=name,
        borderwidth=2,
        relief="ridge",
        width=10
    )
    lbl.grid(row=i // 4, column=i % 4, padx=5, pady=5)

root.mainloop()
