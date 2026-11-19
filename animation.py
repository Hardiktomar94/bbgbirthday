import math
import random
import tkinter as tk

WIDTH, HEIGHT = 900, 700
random.seed()

root = tk.Tk()
root.title("A Birthday Surprise for Agrima")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()

# Soft pink-to-purple background
top = (255, 239, 248)
bottom = (224, 216, 255)
for y in range(0, HEIGHT, 4):
    t = y / HEIGHT
    color = tuple(
        int(top[i] * (1 - t) + bottom[i] * t)
        for i in range(3)
    )
    canvas.create_rectangle(
        0, y, WIDTH, y + 4,
        fill="#%02x%02x%02x" % color,
        outline=""
    )

# Background sparkles
for _ in range(100):
    x, y = random.randrange(WIDTH), random.randrange(HEIGHT)
    size = random.choice([1, 2, 2, 3])
    canvas.create_oval(
        x, y, x + size, y + size,
        fill=random.choice(["#ffffff", "#fff9e8", "#fceaff"]),
        outline=""
    )

flowers = [
    (250, 300, "lily"), (295, 230, "tulip"), (340, 175, "lily"),
    (385, 245, "tulip"), (430, 155, "lily"), (475, 225, "tulip"),
    (520, 165, "lily"), (565, 235, "tulip"), (610, 300, "lily"),
    (310, 340, "tulip"), (360, 300, "lily"), (415, 340, "tulip"),
    (465, 310, "lily"), (520, 345, "tulip"), (575, 340, "lily"),
    (385, 395, "tulip"), (455, 400, "lily"), (525, 395, "tulip"),
]

pink_colors = ["#ff668f", "#ff8eab", "#ffadc3", "#ffd0de"]
lily_colors = ["#fffdf8", "#fff3f8", "#ffe6ef", "#f5eaff"]
green_colors = ["#43875c", "#55a16c", "#70b77c", "#86c98b"]
targets = []

def add_ellipse_targets(cx, cy, rx, ry, count, colors):
    for _ in range(count):
        angle = random.random() * math.tau
        radius = math.sqrt(random.random())
        targets.append((
            cx + math.cos(angle) * rx * radius,
            cy + math.sin(angle) * ry * radius,
            random.choice(colors)
        ))

def add_line_targets(x1, y1, x2, y2, count, color):
    for _ in range(count):
        t = random.random()
        targets.append((
            x1 + (x2 - x1) * t + random.uniform(-2, 2),
            y1 + (y2 - y1) * t + random.uniform(-2, 2),
            color
        ))

# Flower petals and centers
for x, y, kind in flowers:
    colors = lily_colors if kind == "lily" else pink_colors
    for petal in range(6):
        angle = math.radians(petal * 60)
        px = x + math.cos(angle) * 15
        py = y + math.sin(angle) * 15
        add_ellipse_targets(px, py, 18, 9, 7, colors)
    add_ellipse_targets(x, y, 6, 6, 6, ["#ffd36b", "#ffe995"])

# Stems
for x, y, _kind in flowers:
    base_x = 450 + (x - 450) * 0.22
    add_line_targets(base_x, 535, x, y + 18, 10, "#4b9b68")

# Leaves
leaf_positions = [
    (295, 430, -20), (340, 375, 25), (380, 455, 20),
    (420, 405, -25), (475, 455, 25), (515, 405, -25),
    (565, 450, 25), (610, 410, -20), (365, 335, -25),
    (550, 335, 25), (430, 365, 25), (500, 360, -25),
]
for x, y, angle in leaf_positions:
    radians = math.radians(angle)
    for _ in range(9):
        t = random.uniform(-1, 1)
        across = random.uniform(-1, 1)
        targets.append((
            x + math.cos(radians) * t * 28 - math.sin(radians) * across * 8,
            y + math.sin(radians) * t * 28 + math.cos(radians) * across * 8,
            random.choice(green_colors)
        ))

# Dust forms the bouquet's wrapping paper
for _ in range(120):
    y = random.uniform(490, 610)
    half_width = (y - 490) * 0.43 + 10
    x = random.uniform(450 - half_width, 450 + half_width)
    targets.append((x, y, random.choice(["#f0a8c6", "#ffc5dc", "#ffd8e7"])))

# Scattered particles
particles = []
for target_x, target_y, color in targets:
    start_x = random.uniform(0, WIDTH)
    start_y = random.uniform(0, HEIGHT)
    radius = random.choice([2, 2, 3])
    particle_id = canvas.create_oval(
        start_x, start_y,
        start_x + radius, start_y + radius,
        fill=color, outline=""
    )
    particles.append({
        "id": particle_id,
        "x": start_x,
        "y": start_y,
        "start_x": start_x,
        "start_y": start_y,
        "target_x": target_x,
        "target_y": target_y,
        "radius": radius,
    })

def oval_points(cx, cy, rx, ry, angle_degrees, steps=28):
    angle = math.radians(angle_degrees)
    points = []
    for i in range(steps):
        t = math.tau * i / steps
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        points.extend([
            cx + x * math.cos(angle) - y * math.sin(angle),
            cy + x * math.sin(angle) + y * math.cos(angle),
        ])
    return points

def draw_leaf(x, y, angle):
    canvas.create_polygon(
        oval_points(x, y, 33, 11, angle),
        fill="#65ad76", outline="#43875c", width=2, smooth=True
    )
    radians = math.radians(angle)
    canvas.create_line(
        x - 27 * math.cos(radians), y - 27 * math.sin(radians),
        x + 27 * math.cos(radians), y + 27 * math.sin(radians),
        fill="#43875c", width=1
    )

def draw_flower(x, y, kind):
    colors = lily_colors if kind == "lily" else pink_colors

    for i in range(6):
        angle = i * 60
        radians = math.radians(angle)
        px = x + math.cos(radians) * 17
        py = y + math.sin(radians) * 17
        canvas.create_polygon(
            oval_points(px, py, 22, 12, angle),
            fill=random.choice(colors),
            outline="#ffffff", width=1, smooth=True
        )

    canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="#ffd36b", outline="")

    if kind == "lily":
        for angle in (20, 90, 160):
            radians = math.radians(angle)
            end_x = x + math.cos(radians) * 22
            end_y = y + math.sin(radians) * 22
            canvas.create_line(x, y, end_x, end_y, fill="#d88a2b", width=2)
            canvas.create_oval(
                end_x - 3, end_y - 3, end_x + 3, end_y + 3,
                fill="#e6a543", outline=""
            )

def draw_wrapper():
    # Open paper cone around the stems
    canvas.create_polygon(
        255, 490, 645, 490, 540, 625, 360, 625,
        fill="#f3b5d0", outline="#d98cad", width=3
    )

    # Folded front flap gives the paper a wrapped-bouquet look
    canvas.create_polygon(
        255, 490, 450, 548, 645, 490, 450, 590,
        fill="#ffdeeb", outline="#d98cad", width=2
    )
    canvas.create_line(450, 548, 450, 590, fill="#e7a2bf", width=2)

    # Ribbon tails and tied bow
    canvas.create_polygon(
        440, 570, 385, 610, 402, 552,
        fill="#d878a2", outline="#bf5d8a", width=2
    )
    canvas.create_polygon(
        460, 570, 515, 610, 498, 552,
        fill="#d878a2", outline="#bf5d8a", width=2
    )
    canvas.create_oval(
        418, 552, 451, 584,
        fill="#e58bb1", outline="#bf5d8a", width=2
    )
    canvas.create_oval(
        449, 552, 482, 584,
        fill="#e58bb1", outline="#bf5d8a", width=2
    )
    canvas.create_oval(
        438, 559, 462, 582,
        fill="#c75b89", outline="#a84973", width=2
    )

def draw_bouquet_details():
    # Draw stems first; the wrapper covers their ends.
    for x, y, _kind in flowers:
        base_x = 450 + (x - 450) * 0.22
        canvas.create_line(
            base_x, 535, x, y + 10,
            fill="#43875c", width=5, smooth=True
        )

    for x, y, angle in leaf_positions:
        draw_leaf(x, y, angle)

    draw_wrapper()

    # Reveal each flower after the wrapping appears.
    def reveal_flower(index=0):
        if index < len(flowers):
            x, y, kind = flowers[index]
            draw_flower(x, y, kind)
            root.after(45, lambda: reveal_flower(index + 1))
        else:
            show_title()

    reveal_flower()

def show_title():
    message = "Happy Birthday bbg (Agrima) ♥"
    title = canvas.create_text(
        WIDTH // 2, 665,
        text="",
        fill="#a53f70",
        font=("Georgia", 27, "bold")
    )

    def type_next(index=0):
        canvas.itemconfigure(title, text=message[:index])
        if index < len(message):
            root.after(65, lambda: type_next(index + 1))

    type_next()

def animate(frame=0):
    # Smoothly gather the dust into the flowers and wrapper.
    progress = min(frame / 95, 1)
    eased = 1 - (1 - progress) ** 3

    for particle in particles:
        particle["x"] = particle["start_x"] + (
            particle["target_x"] - particle["start_x"]
        ) * eased
        particle["y"] = particle["start_y"] + (
            particle["target_y"] - particle["start_y"]
        ) * eased

        r = particle["radius"]
        canvas.coords(
            particle["id"],
            particle["x"], particle["y"],
            particle["x"] + r, particle["y"] + r
        )

    if frame < 95:
        root.after(16, lambda: animate(frame + 1))
    else:
        draw_bouquet_details()

root.after(250, animate)
root.mainloop()
