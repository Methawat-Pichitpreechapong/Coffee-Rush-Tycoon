import tkinter as tk
import os
from PIL import Image, ImageTk

# Import modules from other project files
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

        # 1. Preload standalone ingredient buttons (bottom panel buttons for all 3 zones)
        ing_files = {
            # --- Burger Zone ---
            "ing_bun": "buger_pure.png",      # Bun button image
            "ing_vegetable": "vegetable.png", # Vegetable button image
            "ing_tomato": "tomato.png",       # Tomato button image
            "ing_meat": "meat.png",           # Meat button image
            
            # --- Coffee Zone ---
            "ing_coffee powder": "coffee_powder.png", 
            "ing_cup": "cup.png",
            "ing_milk": "milk.png",
            "ing_water": "water.png",

            # --- Smoothies Zone ---
            "ing_strawberry": "strawberry.png",
            "ing_orange": "orange.png",
            "ing_ice cube": "ice_cube.png",           
            "ing_syrup": "syrup.png"
        }
        for key, filename in ing_files.items():
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                img = Image.open(path).resize((60, 60), Image.Resampling.NEAREST)
                self.image_cache[key] = ImageTk.PhotoImage(img)

        # 2. Preload combined state images for Holding Slots
        # Technique: Set key as "mix_" followed by sorted ingredient names
        burger_states = {
            # ================= 1 Ingredient =================
            "mix_bun": "buger_pure.png",                             # Only Bun
            "mix_meat": "meat.png",                                  # Only Meat
            "mix_tomato": "tomato.png",                              # Only Tomato
            "mix_vegetable": "vegetable.png",                        # Only Vegetable

            # ================= 2 Ingredients =================
            "mix_bun_meat": "burger_meat.png",                       # Bun + Meat
            "mix_bun_vegetable": "burger_vegetable.png",             # Bun + Vegetable
            "mix_bun_tomato": "burger_tomato.png",                   # Bun + Tomato
            "mix_meat_tomato": "meat_tomato.png",                    # Meat + Tomato
            "mix_meat_vegetable": "meat_vegetable.png",              # Meat + Vegetable
            "mix_tomato_vegetable": "vegetable_tomato.png",          # Tomato + Vegetable

            # ================= 3 Ingredients =================
            "mix_bun_meat_tomato": "burger_meat_tomato.png",         # Bun + Meat + Tomato
            "mix_bun_meat_vegetable": "burger_meat_vegetable.png",   # Bun + Meat + Vegetable
            "mix_bun_tomato_vegetable": "burger_vegetable_tomato.png", # Bun + Tomato + Vegetable
            "mix_meat_tomato_vegetable": "meat_vegetable_tomato.png", # Meat + Tomato + Vegetable

            # ================= 4 Ingredients (Complete Recipe) =================
            "menu_burger": "burger.png",                             # Complete Burger ready to serve!
        }

        for key, filename in burger_states.items():
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                # Resize to (50, 50) to prevent the burger image from exceeding the slot frame bounds
                img = Image.open(path).resize((50, 50), Image.Resampling.NEAREST)
                self.image_cache[key] = ImageTk.PhotoImage(img)

        # =========================================================
        # Coffee Zone (All 15 mathematical combinations covered)
        # =========================================================
        coffee_states = {
            # --- 1 Ingredient ---
            "mix_coffee powder": "coffee_powder.png",
            "mix_cup": "cup.png",
            "mix_milk": "milk.png",
            "mix_water": "water.png",

            # --- 2 Ingredients ---
            "mix_coffee powder_cup": "cup_coffee_powder.png",
            "mix_coffee powder_milk": "cup_coffee_powder_milk.png",
            "mix_coffee powder_water": "espresso.png",
            "mix_cup_milk": "cup_milk.png",
            "mix_cup_water": "cup_water.png",
            "mix_milk_water": "water.png",

            # --- 3 Ingredients ---
            "mix_coffee powder_cup_milk": "cup_coffee_powder_milk.png",

            "mix_coffee powder_cup_water": "espresso.png",           # Fallback buffer before final menu conversion
            "menu_espresso": "espresso.png",                         # Complete Espresso recipe!

            "mix_coffee powder_milk_water": "latte.png",
            "mix_cup_milk_water": "cup_water_milk.png",

            # --- 4 Ingredients (Complete Recipe) ---
            "mix_coffee powder_cup_milk_water": "latte.png",         # Safe buffer combination
            "menu_latte": "latte.png",                               # Complete Latte recipe!
        }

        for key, filename in coffee_states.items():
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                img = Image.open(path).resize((50, 50), Image.Resampling.NEAREST)
                self.image_cache[key] = ImageTk.PhotoImage(img)
        # =========================================================

        smoothie_states = {

            "blender_empty": "blender.png",                                  # Empty blender jug (Initial state)

            # --- 1 Ingredient ---
            "mix_ice cube": "blender_ice_cube.png",                          # Blender + Ice cube
            "mix_syrup": "blender_syrup.png",                                # Blender + Syrup
            "mix_strawberry": "blender_strawberry.png",                      # Blender + Strawberry
            "mix_orange": "blender_orange.png",                              # Blender + Orange

            # --- 2 Ingredients ---
            "mix_ice cube_syrup": "blender_ice_syrup.png",                   # Ice cube + Syrup
            "mix_ice cube_strawberry": "blender_ice_strawberry.png",         # Ice cube + Strawberry
            "mix_ice cube_orange": "blender_ice_orange.png",                 # Ice cube + Orange
            "mix_strawberry_syrup": "blender_strawberry_syrup.png",          # Strawberry + Syrup
            "mix_orange_syrup": "blender_orange_syrup.png",                  # Orange + Syrup

            # --- 3 Ingredients (Complete Recipe) ---
            "menu_strawberry smoothie": "strawberry_smoothie.png",           # Complete Strawberry Smoothie ready to pour!
            "menu_orange smoothie": "orange_smoothie.png",                   # Complete Orange Smoothie ready to pour!

        }

        for key, filename in smoothie_states.items():
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                img = Image.open(path).resize((50, 50), Image.Resampling.NEAREST)
                self.image_cache[key] = ImageTk.PhotoImage(img)

        # =========================================================
        # Grill Zone (Preload raw and cooked meat state images)
        # =========================================================
        grill_states = {
            "grill_cooking": "meat.png",        # Raw meat image displayed during cooking progress
            "grill_cooked": "meat_cooked.png",  # Fully cooked meat image (100% progress)
        }
        for key, filename in grill_states.items():
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                # Resize to fit the grill slot dimensions perfectly
                img = Image.open(path).resize((50, 50), Image.Resampling.NEAREST)
                self.image_cache[key] = ImageTk.PhotoImage(img)


        # =========================================================
        # 👥 Customer Zone (Preload normal and VIP character sprites)
        # =========================================================
        customer_files = {
            "cust_normal_1": "normal_customer_1.png",
            "cust_normal_2": "normal_customer_2.png",
            "cust_normal_3": "normal_customer_3.png",
            "cust_vip_1": "vip_customer_1.png",
            "cust_vip_2": "vip_customer_2.png",
            "cust_vip_3": "vip_customer_3.png",
        }
        for key, filename in customer_files.items():
            path = os.path.join(IMAGE_DIR, filename)
            if os.path.exists(path):
                # Resize slightly to maintain clarity and fit the designated counter pathway
                img = Image.open(path).resize((80, 80), Image.Resampling.NEAREST)
                self.image_cache[key] = ImageTk.PhotoImage(img)


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "GameFrame": frame.start_game()
        elif page_name == "StatsFrame": frame.update_stats()
        frame.tkraise()

if __name__ == "__main__":
    app = CoffeeTycoonApp()
    app.mainloop()