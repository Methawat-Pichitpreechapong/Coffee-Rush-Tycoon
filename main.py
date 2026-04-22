import tkinter as tk
import os
from PIL import Image, ImageTk

# ดึงระบบต่างๆ ที่เราแยกไฟล์ไว้มาใช้งาน
from managers import StatsManager, OrderManager
from screens import MainMenuFrame, GameFrame, DifficultyFrame, StatsFrame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

class CoffeeTycoonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("COFFEE RUSH TYCOON - Project")
        
        window_width, window_height = 1000, 750
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.minsize(800, 600)
        self.resizable(True, True)

        self.current_difficulty = "Normal"
        self.current_day = 1 
        
        self.stats_manager = StatsManager()
        self.order_manager = OrderManager()
        
        self.image_cache = {}
        self.preload_images()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenuFrame, GameFrame, DifficultyFrame, StatsFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuFrame")

    def on_closing(self):
        self.stats_manager.save_stats()
        self.destroy()

    def preload_images(self):
        bg_path = os.path.join(IMAGE_DIR, "bg_main.png")
        if os.path.exists(bg_path):
            img = Image.open(bg_path).resize((1000, 750))
            self.image_cache["bg_main"] = ImageTk.PhotoImage(img)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "GameFrame": frame.start_game()
        elif page_name == "StatsFrame": frame.update_stats()
        frame.tkraise()

if __name__ == "__main__":
    app = CoffeeTycoonApp()
    app.mainloop()