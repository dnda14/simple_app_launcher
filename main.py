import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class RoundedWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.overrideredirect(True)
        self.center_window(800,600)
        
        self.wm_attributes("-alpha", 1)
        self.wm_attributes("-transparentcolor", "#2e2e2e")
        
        self.image2 = Image.open(".\\images\\obsidian_icon.png").resize((50, 50)) 
        self.photo = ImageTk.PhotoImage(self.image2)
        
        self.canvas = tk.Canvas(self, width=800, height=600, bg='#2e2e2e', bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.active_frame = None
        self.frames = []
        self.bind("<Right>", self.on_right_arrow)
        
        self.create_rounded_background()
        self.create_content()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_rounded_background(self):
        self.overlay_frame = ctk.CTkFrame(
            self.canvas,
            corner_radius=20,
            fg_color='#202020',
            width=500,
            height=300
        )
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_content(self):
        frame = ctk.CTkFrame(self.overlay_frame, corner_radius=40, fg_color='#101010')  
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        rows = 3
        columns = 3
        
        for row in range(rows):
            for col in range(columns):
                custom_frame = ctk.CTkFrame(
                    frame,
                    corner_radius=20,
                    fg_color='#242424',  # Default color
                    width=100,
                    height=100
                )
                custom_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                self.frames.append(custom_frame)
                
                
                img_label = ctk.CTkLabel(custom_frame, image=self.photo,text="", bg_color='#242424')
                img_label.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
                
        for col in range(columns):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(rows):
            frame.grid_rowconfigure(row, weight=1)
        
        if self.frames:
            self.set_active_frame(self.frames[0])

    def set_active_frame(self, frame):
        """Set the given frame as active and reset others."""
        if self.active_frame:
            self.active_frame.configure(fg_color='#242424')  # Reset color
        self.active_frame = frame
        self.active_frame.configure(fg_color='#4CAF50')  # Change color to indicate active state

    def on_right_arrow(self, event):
        """Handle the Right arrow key event."""
        if self.active_frame:
            index = self.frames.index(self.active_frame)
            next_index = (index + 1) % len(self.frames)
            self.set_active_frame(self.frames[next_index])

if __name__ == "__main__":
    app = RoundedWindow()
    app.mainloop()
