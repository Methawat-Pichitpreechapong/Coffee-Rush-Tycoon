import random

# ==========================================
# ระบบช่องผสมของ (Holding Slot)
# ==========================================
class HoldingSlot:
    def __init__(self, canvas, frame, zone, x1, y1, x2, y2):
        self.canvas = canvas
        self.frame = frame
        self.zone = zone
        self.mix = []
        self.state = "empty" 
        self.recipe_name = None
        
        self.bg = canvas.create_rectangle(x1, y1, x2, y2, fill="#E0E0E0", outline="black", tags="all")
        self.text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text="Empty", font=("Arial", 9, "bold"), fill="gray", tags="all", justify="center")

        self.canvas.tag_bind(self.bg, "<ButtonPress-1>", lambda e: self.frame.start_dragging(e, source=self))
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", lambda e: self.frame.start_dragging(e, source=self))

    def add_item(self, item):
        self.mix.append(item)
        recipe = self.frame.controller.order_manager.identify_recipe(self.mix, self.zone)
        
        if recipe:
            self.state = "ready"
            self.recipe_name = recipe
            self.canvas.itemconfig(self.bg, fill="#A5D6A7") 
            self.canvas.itemconfig(self.text, text=recipe.replace(" ", "\n"), fill="black")
        else:
            self.state = "building"
            self.recipe_name = None
            self.canvas.itemconfig(self.bg, fill="#FFF59D") 
            self.canvas.itemconfig(self.text, text="\n".join(self.mix), fill="black")

    def add_prebuilt_item(self, recipe_name):
        self.state = "ready"
        self.recipe_name = recipe_name
        self.mix = self.frame.controller.order_manager.recipes[recipe_name].copy()
        self.canvas.itemconfig(self.bg, fill="#A5D6A7") 
        self.canvas.itemconfig(self.text, text=recipe_name.replace(" ", "\n"), fill="black")

    def clear(self):
        self.mix = []
        self.state = "empty"
        self.recipe_name = None
        self.canvas.itemconfig(self.bg, fill="#E0E0E0")
        self.canvas.itemconfig(self.text, text="Empty", fill="gray")

# ==========================================
# วัตถุดิบ (Ingredient)
# ==========================================
class Ingredient:
    def __init__(self, canvas, frame, name, x, y, color, custom_cmd=None):
        self.canvas = canvas
        self.frame = frame
        self.name = name
        img = self.frame.controller.image_cache.get(f"ing_{name.lower()}")
        
        cmd = custom_cmd if custom_cmd else lambda e, n=name: self.frame.add_to_mix(n, e.x, e.y)
        
        if img:
            self.id = self.canvas.create_image(x, y, image=img, tags="all")
            self.canvas.tag_bind(self.id, "<Button-1>", cmd)
        else:
            self.id = self.canvas.create_rectangle(x-35, y-25, x+35, y+25, fill=color, outline="black", width=2, tags="all")
            self.text_id = self.canvas.create_text(x, y, text=name, font=("Arial", 10, "bold"), fill="black", tags="all")
            self.canvas.tag_bind(self.id, "<Button-1>", cmd)
            self.canvas.tag_bind(self.text_id, "<Button-1>", cmd)

# ==========================================
# ลูกค้า (Customer)
# ==========================================
class Customer:
    def __init__(self, canvas, frame, target_x, target_y, slot_idx):
        self.canvas = canvas
        self.frame = frame
        self.slot_idx = slot_idx
        
        sx = self.frame.scale_x
        sy = self.frame.scale_y
        
        self.target_x = target_x * sx
        self.y = target_y * sy
        self.x = -150 * sx 
        self.speed = max(1, int(10 * sx)) 
        
        self.menu_id = random.choice(["Latte", "Espresso", "Burger", "Strawberry Smoothie", "Orange Smoothie"])
        self.cust_type = "Normal"
        self.patience = 100
        self.state = "walking" 
        
        self.id = self.canvas.create_oval(self.x-40*sx, self.y-40*sy, self.x+40*sx, self.y+40*sy, fill="#BBDEFB", outline="black", width=max(1, int(2*sx)), tags="all")
        self.order_box = self.canvas.create_rectangle(self.x-70*sx, self.y-85*sy, self.x+70*sx, self.y-55*sy, fill="white", outline="black", tags="all")
        font_size = max(8, int(9 * min(sx, sy)))
        self.order_text = self.canvas.create_text(self.x, self.y-70*sy, text=self.menu_id, font=("Arial", font_size, "bold"), fill="black", tags="all")
        self.bar_bg = self.canvas.create_rectangle(self.x-40*sx, self.y+50*sy, self.x+40*sx, self.y+60*sy, fill="#BDBDBD", tags="all")
        self.bar_fg = self.canvas.create_rectangle(self.x-40*sx, self.y+50*sy, self.x+40*sx, self.y+60*sy, fill="#4CAF50", tags="all")

    def update(self, diff):
        if self.state == "walking":
            self.x += self.speed
            self.canvas.move(self.id, self.speed, 0)
            self.canvas.move(self.order_box, self.speed, 0)
            self.canvas.move(self.order_text, self.speed, 0)
            self.canvas.move(self.bar_bg, self.speed, 0)
            self.canvas.move(self.bar_fg, self.speed, 0)
            
            if self.x >= self.target_x:
                self.state = "waiting" 
                
        elif self.state == "waiting":
            rate = 0.05 if diff == "Easy" else 0.15 if diff == "Normal" else 0.3
            self.patience -= rate
            
            bg_coords = self.canvas.coords(self.bar_bg)
            if not bg_coords: return
            x1, y1, x2, y2 = bg_coords
            width = max(0, (self.patience / 100) * (x2 - x1))
            self.canvas.coords(self.bar_fg, x1, y1, x1 + width, y2)
            if self.patience < 30: self.canvas.itemconfig(self.bar_fg, fill="#F44336")

    def clear(self):
        self.canvas.delete(self.id, self.order_box, self.order_text, self.bar_bg, self.bar_fg)