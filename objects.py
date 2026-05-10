import random


# ==========================================
# Holding Slot System - Upgraded to support Pixel Art state stacking
# ==========================================
class HoldingSlot:
    def __init__(self, canvas, frame, zone, x1, y1, x2, y2):
        self.canvas = canvas
        self.frame = frame
        self.zone = zone
        self.mix = []
        self.state = "empty" 
        self.recipe_name = None
        self.img_id = None  # Reference variable to store the displayed Pixel Art image ID
        
        self.bg = canvas.create_rectangle(x1, y1, x2, y2, fill="#E0E0E0", outline="black", tags="all")
        self.text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text="Empty", font=("Arial", 9, "bold"), fill="gray", tags="all", justify="center")

        self.canvas.tag_bind(self.bg, "<ButtonPress-1>", lambda e: self.frame.start_dragging(e, source=self))
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", lambda e: self.frame.start_dragging(e, source=self))

    def update_visual(self):
        """ Updates the slot's GUI representation while maintaining 100% core game logic """
        # 1. Remove previous image representation (if any)
        if self.img_id:
            self.canvas.delete(self.img_id)
            self.img_id = None

        # 2. Search for the appropriate state image from Cache based on combined ingredients
        img = None
        cache = self.frame.controller.image_cache

        if self.state == "ready" and self.recipe_name:
            # Fully assembled menu item (e.g., "menu_burger")
            img = cache.get(f"menu_{self.recipe_name.lower()}")
        elif self.state == "building" and self.mix:
            # Sort raw ingredient names alphabetically to fetch stacking key (e.g., ['Bun', 'Meat'] -> "mix_bun_meat")
            sorted_mix = "_".join(sorted([m.lower() for m in self.mix]))
            img = cache.get(f"mix_{sorted_mix}")

        # 3. Render updates onto the canvas
        if img:
            # Hide standard label text and place the Pixel Art centered on the slot
            self.canvas.itemconfig(self.text, text="")
            coords = self.canvas.coords(self.bg)
            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            self.img_id = self.canvas.create_image(center_x, center_y, image=img, tags="all")
            # Bind dragging/serving triggers directly to the newly spawned image
            self.canvas.tag_bind(self.img_id, "<ButtonPress-1>", lambda e: self.frame.start_dragging(e, source=self))
        else:
            # Safe Fallback: If an image key is missing, revert gracefully to standard colors and plain text
            if self.state == "ready":
                self.canvas.itemconfig(self.bg, fill="#A5D6A7")
                self.canvas.itemconfig(self.text, text=self.recipe_name.replace(" ", "\n"), fill="black")
            elif self.state == "building":
                self.canvas.itemconfig(self.bg, fill="#FFF59D")
                self.canvas.itemconfig(self.text, text="\n".join(self.mix), fill="black")
            else:
                self.canvas.itemconfig(self.bg, fill="#E0E0E0")
                self.canvas.itemconfig(self.text, text="Empty", fill="gray")

    def add_item(self, item):
        self.mix.append(item)
        recipe = self.frame.controller.order_manager.identify_recipe(self.mix, self.zone)

        if recipe:
            self.state = "ready"
            self.recipe_name = recipe
        else:
            self.state = "building"
            self.recipe_name = None

        self.update_visual()  # Trigger GUI update

    def add_prebuilt_item(self, recipe_name):
        self.state = "ready"
        self.recipe_name = recipe_name
        self.mix = self.frame.controller.order_manager.recipes[recipe_name].copy()
        self.update_visual()  # Trigger GUI update

    def clear(self):
        self.mix = []
        self.state = "empty"
        self.recipe_name = None
        self.update_visual()  # Trigger GUI update

# ==========================================
# Raw Ingredient Button Representation (Always renders a background border frame)
# ==========================================
class Ingredient:
    def __init__(self, canvas, frame, name, x, y, color, custom_cmd=None):
        self.canvas = canvas
        self.frame = frame
        self.name = name
        img = self.frame.controller.image_cache.get(f"ing_{name.lower()}")
        
        cmd = custom_cmd if custom_cmd else lambda e, n=name: self.frame.add_to_mix(n, e.x, e.y)
        
        # 1. Always draw a solid background rectangle with a distinct border to prevent floating visuals
        self.bg_box = self.canvas.create_rectangle(x-35, y-30, x+35, y+30, fill=color, outline="black", width=2, tags="all")
        self.canvas.tag_bind(self.bg_box, "<Button-1>", cmd)

        if img:
            # 2. If a Pixel Art image exists, place it directly over the background frame
            self.id = self.canvas.create_image(x, y, image=img, tags="all")
            self.canvas.tag_bind(self.id, "<Button-1>", cmd)
        else:
            # 3. Fallback to standard text representation if the image is missing
            self.text_id = self.canvas.create_text(x, y, text=name, font=("Arial", 10, "bold"), fill="black", tags="all")
            self.canvas.tag_bind(self.text_id, "<Button-1>", cmd)

# ==========================================
# Customer Representation (Replaced plain ovals with custom character sprites)
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
        
        cache = self.frame.controller.image_cache
        img = None
        
        # 25% chance to spawn a VIP customer yielding double revenue multipliers
        if random.random() < 0.25:
            self.cust_type = "VIP"
            # Randomly select among the 3 loaded VIP sprites (with yellow outlines)
            sprite_key = random.choice(["cust_vip_1", "cust_vip_2", "cust_vip_3"])
            img = cache.get(sprite_key)
        else:
            self.cust_type = "Normal"
            # Randomly select among the 3 loaded Normal sprites (without outlines)
            sprite_key = random.choice(["cust_normal_1", "cust_normal_2", "cust_normal_3"])
            img = cache.get(sprite_key)
            
        self.patience = 100
        self.state = "walking" 
        
        if img:
            # Render the assigned custom Pixel Art character directly onto the pathway
            self.id = self.canvas.create_image(self.x, self.y, image=img, tags="all")
        else:
            # Safe Fallback: Revert to colored ovals if character image keys are missing
            fill_c = "#FFF9C4" if self.cust_type == "VIP" else "#BBDEFB"
            outl_c = "#FF9800" if self.cust_type == "VIP" else "black"
            self.id = self.canvas.create_oval(self.x-40*sx, self.y-40*sy, self.x+40*sx, self.y+40*sy, fill=fill_c, outline=outl_c, width=max(1, int(2*sx)), tags="all")
            
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