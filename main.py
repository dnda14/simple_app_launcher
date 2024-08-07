import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def rgb_to_hex(rgb):
    """Convierte una tupla RGB (rojo, verde, azul) a un formato hexadecimal"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def create_blur_border_image(size, color, blur_radius):
    """Crea una imagen con un borde difuso"""
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dibuja un rectángulo con borde difuso
    draw.rectangle([(0, 0), (size[0] - 1, size[1] - 1)], outline=color, width=blur_radius)
    
    return image

def create_grid(window, rows, columns):
    frame = tk.Frame(window, bg=rgb_to_hex([255,255,255]))
    frame.pack(expand=True, fill=tk.BOTH)

    buttons = []
    for row in range(rows):
        for col in range(columns):
            button = tk.Button(frame, text="", width=10, height=5, bg="lightgray")
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            buttons.append(button)

    buttons[0].config(bg="lightblue", borderwidth=5)
    
    for col in range(columns):
        frame.grid_columnconfigure(col, weight=1)
    for row in range(rows):
        frame.grid_rowconfigure(row, weight=1)

    return buttons

def highlight_cell(button, frame):
    """Aplica un efecto de borde difuso a la celda seleccionada"""
    button.config(bg=rgb_to_hex((100, 100, 100)), fg=rgb_to_hex((255, 255, 255)),
                  relief="flat")

    canvas = tk.Canvas(frame, width=button.winfo_reqwidth(), height=button.winfo_reqheight(), bg=rgb_to_hex((0, 0, 0)), bd=0, highlightthickness=0)
    canvas.grid(row=button.grid_info()['row'], column=button.grid_info()['column'], padx=5, pady=5, sticky="nsew")

    blur_image = create_blur_border_image((button.winfo_reqwidth(), button.winfo_reqheight()), rgb_to_hex((128, 128, 128)), 10)
    blur_image_tk = ImageTk.PhotoImage(blur_image)
    
    canvas.create_image(0, 0, anchor=tk.NW, image=blur_image_tk)
    canvas.image = blur_image_tk   



def close_window(event):
    root.destroy()

root = tk.Tk()
root.title("Lanzador de Aplicaciones")
root.configure(bg=rgb_to_hex((0, 0, 0)))
rows = 3
columns = 3
buttons = create_grid(root, rows, columns)

root.bind("<Return>", close_window)

root.mainloop()
