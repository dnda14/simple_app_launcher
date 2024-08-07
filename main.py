import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw

class RoundedWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.overrideredirect(True)  # Elimina la barra de título y bordes de la ventana
        self.configure(fg_color='#2e2e2e')  # Color de fondo de la ventana
        self.center_window(800,600)
        
        self.wm_attributes("-alpha", 0.85)
        self.wm_attributes("-transparentcolor", "#2e2e2e")
        
        # Crear un lienzo para el fondo redondeado
        self.canvas = tk.Canvas(self, width=800, height=600, bg='#2e2e2e', bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Crear la imagen redondeada para el fondo
        #self.create_rounded_background()

        # Crear el contenido de la ventana
        self.create_content()
        # Manejador de eventos para mover la ventana
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)

    def center_window(self, width, height):
        """Centrar la ventana en la pantalla"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_rounded_background(self):
        """Crea una imagen con bordes redondeados y la establece como fondo del lienzo"""
        radius = 30
        size = (400, 300)
        image = Image.new("RGBA", size, (150, 150, 0, 0))
        draw = ImageDraw.Draw(image)

        # Dibuja los bordes redondeados
        draw.rectangle([radius, 0, size[0] - radius, size[1]], fill='#090909')
        draw.rectangle([0, radius, size[0], size[1] - radius], fill='#a0a0a0')
        draw.ellipse([0, 0, radius * 2, radius * 2], fill='#a0a0a0')
        draw.ellipse([size[0] - radius * 2, 0, size[0], radius * 2], fill='#2e2e2e')
        draw.ellipse([0, size[1] - radius * 2, radius * 2, size[1]], fill='#2e2e2e')
        draw.ellipse([size[0] - radius * 2, size[1] - radius * 2, size[0], size[1]], fill='#2e2e2e')

        # Convertir la imagen a PhotoImage y establecerla en el lienzo
        rounded_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=rounded_image)
        self.canvas.image = rounded_image

    def create_content(self):
        """Crea el contenido de la ventana, como botones y etiquetas"""
        # Crear un marco en el lienzo para el contenido
        frame = ctk.CTkFrame(self.canvas, corner_radius=40, fg_color='#1e1e1e')  # Color de fondo gris más oscuro
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        rows = 3
        columns=3
        buttons=[]
        
        # Crear un botón con estilo personalizado
        for row in range(rows):
            for col in range(columns):
                button = ctk.CTkButton(frame, text=f"Botón {row * columns + col + 1}", width=80, height=40, fg_color='#4CAF50')  # Color de fondo verde
                button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                buttons.append(button)

        # Configurar el grid para que las filas y columnas se estiren
        for col in range(columns):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(rows):
            frame.grid_rowconfigure(row, weight=1)
            
        image = Image.open(".\images\obsidian_icon.png").resize((600, 600))
        
            
        photo = ImageTk.PhotoImage(image)
        
        # Coloca la imagen en el canvas
        self.canvas.create_image(0, 0, image=photo, anchor='nw')

        # Mantener una referencia a la imagen para evitar la recolección de basura
        self.canvas.image = photo
                
    def start_move(self, event):
        """Comienza a mover la ventana"""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Mueve la ventana"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.geometry(f'+{self.winfo_x() + deltax}+{self.winfo_y() + deltay}')

if __name__ == "__main__":
    app = RoundedWindow()
    app.mainloop()
