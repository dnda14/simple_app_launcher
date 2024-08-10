import tkinter as tk
from time import strftime

import customtkinter as ctk
from PIL import Image, ImageTk

class ClockFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self, text="", font=("Arial", 80), text_color="#cc00ff", fg_color='#242424')
        self.label.pack(expand=True, fill=tk.BOTH)
        self.update_time()

    def update_time(self):
        now = strftime("%H:%M:%S")          
        self.label.configure(text=now)
        self.after(1000, self.update_time) 
        
def read_data_from_file(filename):
    items = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                logo, nombre, ubicacion = parts
                items.append({"logo": logo, "nombre": nombre, "ubicacion": ubicacion})
    size = len(items)
    exc_size = (size // 3 + 1) if size % 3 != 0 else size // 3
    items.extend([{"logo": "", "nombre": "", "ubicacion": ""}] * (exc_size * 3 - size))

    list_group_three = [items[i : i + 3] for i in range(0, len(items), 3)]

    return list_group_three


class GridFrame(ctk.CTkFrame):
    def __init__(self, master=None, color="#242424", items=None, **kwargs):
        super().__init__(master, **kwargs)
        self.color = color
        self.list_items = items if items else []
        self.image_references = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.create_grid_items()

    def create_grid_items(self):
        for i, item in enumerate(self.list_items):
            cell_frame = ctk.CTkFrame(
                self, corner_radius=10, fg_color="#242424", width=100, height=100
            )
            cell_frame.grid(row=0, column=i, padx=0, pady=0, sticky="nsew")
            
            cell_frame.grid_rowconfigure(0, weight=1)
            cell_frame.grid_rowconfigure(1, weight=1)
            cell_frame.grid_columnconfigure(0, weight=1)
            
            logo_frame = ctk.CTkFrame(
                cell_frame, corner_radius=10, fg_color=self.color, width=100, height=100
            )
            logo_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            logo_frame.grid_rowconfigure(0, weight=1)
            logo_frame.grid_columnconfigure(0, weight=1)

            logo_image_path = str(item.get("logo"))
            if logo_image_path != "":
                image_logo = Image.open(logo_image_path).resize((100, 100))

                photo = ImageTk.PhotoImage(image_logo)
                label_logo = ctk.CTkLabel(
                    logo_frame, image=photo, text="", bg_color="#242424"
                )
            else:
                label_logo = ctk.CTkLabel(logo_frame, text="", bg_color="#242424")
            
            label_logo.grid(row=0,column=0,padx=0, pady=0, sticky="nsew")
            label_logo.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)

            title_frame = ctk.CTkFrame(
                cell_frame, corner_radius=10, fg_color="#242424", width=130, height=0
            )
            title_frame.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")
            label_title = ctk.CTkLabel(
                title_frame, text=item.get("nombre", f"Item {i+1}"), font=("Arial", 20), text_color="#cc00ff"
            )
            label_title.pack(expand=True, fill=tk.BOTH, padx=0, pady=0)


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        #self.title("GridFrame Example")
        self.overrideredirect(True)
        self.center_window(450, 450)
        self.wm_attributes("-alpha", 1)
        self.wm_attributes("-transparentcolor", "#ffffff")
        
        #self.base_layer = tk.Canvas(self, width=800, height=800, bg='#2a2e2e', bd=0, highlightthickness=0)
        #self.base_layer.pack(expand=True, fill=tk.BOTH)
        self.base_layer = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color='#ffffff',
            bg_color='#ffffff',
            width=400,
            height=400
        )
        self.base_layer.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.create_grid_layer()
        self.create_clock()
        items = read_data_from_file("config.txt")

        self.lista_grid = []
        self.n_rows = len(items)
        for i in range(self.n_rows):
            self.lista_grid.append(
                GridFrame(
                    self.flayer_frame2,
                    color="#000000",
                    items=items[i],
                    corner_radius=20,
                    fg_color="#242424",
                )
            )

        self.current_position = 0
        self.current_frame = self.lista_grid[self.current_position]
        self.lista_grid[self.current_position].pack(
            expand=True, fill=tk.BOTH, padx=0, pady=20
        )

        self.bind("<Up>", self.show_frame_below)
        self.bind("<Down>", self.show_frame_up)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.config(bg='#ffffff')
    
    
    def show_frame_below(self, event):
        self.current_position = (self.current_position + 1) % self.n_rows
        self.switch_frame(self.lista_grid[self.current_position])

    def show_frame_up(self, event):
        self.current_position = (self.current_position - 1) % self.n_rows
        self.switch_frame(self.lista_grid[self.current_position])

    def switch_frame(self, new_frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = new_frame
        self.current_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def create_grid_layer(self):
        self.flayer_frame1 = ctk.CTkFrame(
            self.base_layer,
            corner_radius=20,
            fg_color='#242424',  
            width=400,
            height=100
        )
        self.flayer_frame1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.base_layer.grid_columnconfigure(0, weight=1)
        self.base_layer.grid_rowconfigure(0, weight=1)
        
        self.flayer_frame2 = ctk.CTkFrame(
            self.base_layer,
            corner_radius=20,
            fg_color='#242424',  
            width=400,
            height=300
        )
        self.flayer_frame2.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.base_layer.grid_columnconfigure(0, weight=1)
        self.base_layer.grid_rowconfigure(1, weight=1)
    
    def create_clock(self):
        clock_frame = ClockFrame(self.flayer_frame1, corner_radius=40, fg_color='#101010', width=200, height=100)
        clock_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
