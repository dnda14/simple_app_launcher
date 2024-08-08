import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class RoundedWindow(ctk.CTk):
    image2 = Image.open(".\\images\\obsidian_icon.png").resize((50, 50)) 
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.overrideredirect(True)  
        self.center_window(800,600)
        
        self.wm_attributes("-alpha", 1)
        self.wm_attributes("-transparentcolor", "#2e2e2e")
        
        self.canvas = tk.Canvas(self, width=800, height=600, bg='#2e2e2e', bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.create_content()
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
        self.overlay_frame = ctk.CTkFrame(
            self.canvas,
            corner_radius=20,  
            fg_color='#ffffff',  
            width=500,         
            height=300
        )
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        
    def create_content(self):
        frame = ctk.CTkFrame(self.canvas, corner_radius=40, fg_color='#00ee00')  
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        rows = 3
        columns=3
        buttons=[]
        
        for row in range(rows):
            for col in range(columns):
                photo = ImageTk.PhotoImage(self.image2)
                button = ctk.CTkButton(
                    frame,
                    text="",  
                    image=photo,
                    corner_radius=20,  
                    width=80,  
                    height=80, 
                    fg_color='#242424',  
                    hover_color='#4CAF50'  
                )
                button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                buttons.append(button)

        for col in range(columns):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(rows):
            frame.grid_rowconfigure(row, weight=1)
                
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.geometry(f'+{self.winfo_x() + deltax}+{self.winfo_y() + deltay}')

if __name__ == "__main__":
    app = RoundedWindow()
    app.mainloop()
