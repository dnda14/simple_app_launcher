import tkinter as tk
from time import strftime
import customtkinter as ctk
from PIL import Image, ImageTk

class ClockFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text="", font=("Arial", 80), fg_color='#101010')
        self.label.pack(expand=True, fill=tk.BOTH)
        self.update_time()

    def update_time(self):
        now = strftime("%H:%M:%S")  
        self.label.configure(text=now)
        self.after(1000, self.update_time) 


class RoundedWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.overrideredirect(True)
        self.center_window(800, 800)
        
        self.wm_attributes("-alpha", 1)
        self.wm_attributes("-transparentcolor", "#2e2e2e")
        
        self.image2 = Image.open(".\\assets\\obsidian_icon.png").resize((50, 50)) 
        self.photo = ImageTk.PhotoImage(self.image2)
        
        self.canvas = tk.Canvas(self, width=800, height=800, bg='#2e2e2e', bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.active_frame = None
        self.frames = []
        self.bind("<Right>", self.on_right_arrow)
        self.bind("<Left>", self.on_left_arrow)
        
        self.create_background()
        self.create_first_layer()
        self.create_clock()
        self.create_content_from_file("config.txt")

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_background(self):
        self.background_frame = ctk.CTkFrame(
            self.canvas,
            corner_radius=20,
            fg_color='#202020',
            width=800,
            height=800
        )
        self.background_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_first_layer(self):
        self.flayer_frame1 = ctk.CTkFrame(
            self.background_frame,
            corner_radius=20,
            fg_color='#242424',  
            width=400,
            height=100
        )
        self.flayer_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.background_frame.grid_columnconfigure(0, weight=1)
        self.background_frame.grid_rowconfigure(0, weight=1)
        
        self.flayer_frame2 = ctk.CTkFrame(
            self.background_frame,
            corner_radius=20,
            fg_color='#242424',  
            width=400,
            height=300
        )
        self.flayer_frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.background_frame.grid_columnconfigure(0, weight=1)
        self.background_frame.grid_rowconfigure(1, weight=1)
        
    def create_clock(self):
        clock_frame = ClockFrame(self.flayer_frame1, corner_radius=40, fg_color='#101010', width=200, height=100)
        clock_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_content_from_file(self, filename):
        #with open(filename, 'r') as file:
         
         #   rows = int(file.readline().strip())
        
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        rows = len(lines)
        columns = 3
        
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()
        
        for row in range(rows):
            for col in range(columns):
                custom_frame = ctk.CTkFrame(
                    self.flayer_frame2,
                    corner_radius=20,
                    fg_color='#242424',  
                    width=100,
                    height=100
                )
                custom_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                self.frames.append(custom_frame)
                
                img_label = ctk.CTkLabel(custom_frame, image=self.photo, text="", bg_color='#242424')
                img_label.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
                
        for col in range(columns):
            self.flayer_frame2.grid_columnconfigure(col, weight=1)
        for row in range(rows):
            self.flayer_frame2.grid_rowconfigure(row, weight=1)
        
        if self.frames:
            self.set_active_frame(self.frames[0])

    def set_active_frame(self, frame):
        if self.active_frame:
            self.active_frame.configure(fg_color='#242424')  
        self.active_frame = frame
        self.active_frame.configure(fg_color='#3e3e3e')  

    def on_right_arrow(self, event):
        if self.active_frame:
            index = self.frames.index(self.active_frame)
            next_index = (index + 1) % len(self.frames)
            self.set_active_frame(self.frames[next_index])
            
    def on_left_arrow(self, event):
        if self.active_frame:
            index = self.frames.index(self.active_frame)
            prev_index = (index - 1) % len(self.frames)
            self.set_active_frame(self.frames[prev_index])

if __name__ == "__main__":
    app = RoundedWindow()
    app.mainloop()
