import tkinter as tk
import customtkinter as ctk

def read_data_from_file(filename):
    items = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                logo, nombre, ubicacion = parts
                items.append({
                    'logo': logo,
                    'nombre': nombre,
                    'ubicacion': ubicacion
                })
    size = len(items)
    exc_size = (size//3+1) if size%3 != 0 else size//3 
    items.extend([{'logo': '', 'nombre': '', 'ubicacion': ''}] * (exc_size * 3 - size))
    
    list_group_three = [items[i:i + 3] for i in range(0, len(items), 3)]
    
    return list_group_three


class GridFrame(ctk.CTkFrame):
    def __init__(self, master=None, color='#eeeeee', items=None, **kwargs):
        super().__init__(master, **kwargs)
        self.color = color  
        self.list_items = items if items else []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.create_grid_items()
        
    def create_grid_items(self):
        for i, item in enumerate(self.list_items):
            cell_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.color, width=100, height=100)
            cell_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            logo_frame = ctk.CTkFrame(cell_frame, corner_radius=10, fg_color=self.color, width=100, height=100)
            logo_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            label_logo = ctk.CTkLabel(logo_frame, text=item.get('logo',f"Item {i+1}"))
            label_logo.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            title_frame = ctk.CTkFrame(cell_frame, corner_radius=10, fg_color=self.color, width=100, height=100)
            title_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            label_title = ctk.CTkLabel(title_frame, text=item.get('nombre',f"Item {i+1}"))
            label_title.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
           

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GridFrame Example")
        self.geometry("600x200")
        
        items = read_data_from_file('config.txt')
        print(items)
        self.lista_grid=[]
        self.n_rows=len(items)
        for i in range(self.n_rows):
            self.lista_grid.append(GridFrame(self, color="#000000", items=items[i], corner_radius=20, fg_color="#cccccc"))
        print(self.n_rows)
        self.current_position = 0
        self.current_frame = self.lista_grid[self.current_position]
        self.lista_grid[self.current_position].pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.bind("<Up>", self.show_frame_below)
        self.bind("<Down>", self.show_frame_up)
    
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

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
