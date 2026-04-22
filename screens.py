import tkinter as tk
from tkinter import ttk
import random

# อิมพอร์ตคลาสจากไฟล์ objects.py
from objects import HoldingSlot, Ingredient, Customer

class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#D7CCC8")
        self.controller = controller
        bg_img = self.controller.image_cache.get("bg_main")
        if bg_img: tk.Label(self, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        title_bg = tk.Frame(self, bg="#D7CCC8", padx=20, pady=10) 
        title_bg.place(relx=0.5, rely=0.2, anchor="center")
        tk.Label(title_bg, text="☕ COFFEE RUSH TYCOON", font=("Arial", 38, "bold"), bg="#D7CCC8", fg="black").pack()

        btn_y = 0.5
        for text, cmd_frame, color in [("▶ START GAME", "GameFrame", "#4CAF50"), 
                                       ("⚙ DIFFICULTY", "DifficultyFrame", "#FF9800"), 
                                       ("📊 VIEW STATS", "StatsFrame", "#2196F3")]:
            btn = tk.Label(self, text=text, font=("Arial", 20, "bold"), bg=color, fg="black", width=18, pady=12, cursor="hand2", relief="raised", bd=2)
            btn.place(relx=0.5, rely=btn_y, anchor="center")
            btn.bind("<Button-1>", lambda e, f=cmd_frame: self.controller.show_frame(f))
            btn_y += 0.12

class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.base_w, self.base_h = 1000, 750
        
        self.scale_x = 1.0
        self.scale_y = 1.0

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.holding_slots = []
        self.blenders = []
        self.grills = []
        
        self.setup_layout()
        self.canvas.bind("<Configure>", self.on_resize)

        self.cash = 0
        self.customer_slots = [None, None, None]
        self.is_playing = False
        self.is_paused = False
        self.is_dragging = False
        self.drag_source = None
        self.after_id = None
        self.timer_id = None
        
        self.time_left = 120
        self.daily_earned = 0
        self.daily_success = 0
        self.daily_fail = 0

    def update_cash(self, amount):
        self.cash += amount
        self.canvas.itemconfig(self.cash_text, text=f"CASH: ${self.cash}")

    def setup_layout(self):
        self.canvas.create_rectangle(0, 0, 1000, 350, fill="#E0F2F1", outline="", tags="all")
        
        self.day_text = self.canvas.create_text(50, 70, text="DAY: 1", font=("Arial", 24, "bold"), fill="#E65100", anchor="w", tags="all")
        self.cash_text = self.canvas.create_text(500, 70, text=f"CASH: $0", font=("Arial", 28, "bold"), fill="black", anchor="center", tags="all")
        self.timer_text = self.canvas.create_text(950, 70, text="TIME: 02:00", font=("Arial", 24, "bold"), fill="#D32F2F", anchor="e", tags="all")

        tk.Button(self, text="⬅ EXIT GAME", font=("Arial", 10, "bold"), fg="black", command=self.stop_game).place(x=10, y=10)
        self.btn_pause = tk.Button(self, text="⏸ PAUSE", font=("Arial", 10, "bold"), fg="black", command=self.toggle_pause)
        self.btn_pause.place(x=140, y=10)
        tk.Button(self, text="ⓘ RECIPES", font=("Arial", 10, "bold"), fg="black", command=self.show_recipes).place(relx=0.98, y=10, anchor="ne")

        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)

        self.canvas.create_rectangle(0, 350, 1000, 750, fill="#FAFAFA", outline="black", width=2, tags="all")
        self.canvas.create_line(333, 350, 333, 750, fill="black", width=4, tags="all")
        self.canvas.create_line(666, 350, 666, 750, fill="black", width=4, tags="all")

        self.canvas.create_text(166, 380, text="🥤 SMOOTHIES Zone", font=("Arial", 14, "bold"), fill="black", tags="all")
        self.canvas.create_rectangle(50, 410, 210, 550, outline="black", width=2, tags="all")
        
        jug1 = self.canvas.create_oval(70, 420, 110, 500, fill="#CFD8DC", tags="all")
        self.canvas.create_rectangle(70, 500, 110, 540, fill="gray", tags="all")
        text1 = self.canvas.create_text(90, 460, text="", font=("Arial", 8, "bold"), fill="black", tags="all", state="hidden", justify="center")

        jug2 = self.canvas.create_oval(150, 420, 190, 500, fill="#CFD8DC", tags="all")
        self.canvas.create_rectangle(150, 500, 190, 540, fill="gray", tags="all")
        text2 = self.canvas.create_text(170, 460, text="", font=("Arial", 8, "bold"), fill="black", tags="all", state="hidden", justify="center")

        self.blenders = [
            {"bg_id": jug1, "text_id": text1, "state": "empty", "mix": [], "recipe_name": None, "progress": 0},
            {"bg_id": jug2, "text_id": text2, "state": "empty", "mix": [], "recipe_name": None, "progress": 0}
        ]
        
        self.canvas.tag_bind(jug1, "<Button-1>", lambda e, b=self.blenders[0]: self.pickup_blended_smoothie(b, e))
        self.canvas.tag_bind(text1, "<Button-1>", lambda e, b=self.blenders[0]: self.pickup_blended_smoothie(b, e))
        self.canvas.tag_bind(jug2, "<Button-1>", lambda e, b=self.blenders[1]: self.pickup_blended_smoothie(b, e))
        self.canvas.tag_bind(text2, "<Button-1>", lambda e, b=self.blenders[1]: self.pickup_blended_smoothie(b, e))

        self.holding_slots.append(HoldingSlot(self.canvas, self, "Smoothies", 235, 415, 305, 455))
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Smoothies", 235, 460, 305, 500))
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Smoothies", 235, 505, 305, 545))
        
        Ingredient(self.canvas, self, "Strawberry", 45, 620, "#E91E63")
        Ingredient(self.canvas, self, "Orange", 125, 620, "#FF9800")
        Ingredient(self.canvas, self, "Ice cube", 205, 620, "#E0F7FA")
        Ingredient(self.canvas, self, "Syrup", 285, 620, "#FFC107")

        self.trash_box = self.canvas.create_rectangle(20, 690, 110, 730, fill="#F44336", outline="black", width=2, tags="all")
        self.trash_text = self.canvas.create_text(65, 710, text="TRASH", fill="black", font=("Arial", 10, "bold"), tags="all")

        self.canvas.create_text(500, 380, text="☕ COFFEE Zone", font=("Arial", 14, "bold"), fill="black", tags="all")
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Coffee", 365, 415, 450, 475))
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Coffee", 455, 415, 540, 475))
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Coffee", 545, 415, 630, 475))

        Ingredient(self.canvas, self, "Coffee Powder", 440, 540, "#795548")
        Ingredient(self.canvas, self, "Cup", 560, 540, "#FAFAFA")
        Ingredient(self.canvas, self, "Milk", 440, 630, "#FFFFFF")
        Ingredient(self.canvas, self, "Water", 560, 630, "#A4DDED")

        self.canvas.create_text(833, 380, text="🍔 BURGER Zone", font=("Arial", 14, "bold"), fill="black", tags="all")
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Burger", 695, 415, 785, 475))
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Burger", 790, 415, 880, 475))
        self.holding_slots.append(HoldingSlot(self.canvas, self, "Burger", 885, 415, 975, 475))

        self.canvas.create_rectangle(710, 500, 780, 580, fill="#CFD8DC", outline="black", tags="all")
        self.canvas.create_text(745, 565, text="ที่ทอด", font=("Arial", 9), fill="black", tags="all")
        meat1 = self.canvas.create_oval(720, 510, 770, 560, fill="#E57373", tags="all", state="hidden")
        text1 = self.canvas.create_text(745, 535, text="0%", font=("Arial", 8, "bold"), fill="white", tags="all", state="hidden")

        self.canvas.create_rectangle(790, 500, 860, 580, fill="#CFD8DC", outline="black", tags="all")
        self.canvas.create_text(825, 565, text="ที่ทอด", font=("Arial", 9), fill="black", tags="all")
        meat2 = self.canvas.create_oval(800, 510, 850, 560, fill="#E57373", tags="all", state="hidden")
        text2 = self.canvas.create_text(825, 535, text="0%", font=("Arial", 8, "bold"), fill="white", tags="all", state="hidden")

        self.canvas.create_rectangle(870, 500, 940, 580, fill="#CFD8DC", outline="black", tags="all")
        self.canvas.create_text(905, 565, text="ที่ทอด", font=("Arial", 9), fill="black", tags="all")
        meat3 = self.canvas.create_oval(880, 510, 930, 560, fill="#E57373", tags="all", state="hidden")
        text3 = self.canvas.create_text(905, 535, text="0%", font=("Arial", 8, "bold"), fill="white", tags="all", state="hidden")

        self.grills = [
            {"meat_id": meat1, "text_id": text1, "state": "empty", "progress": 0},
            {"meat_id": meat2, "text_id": text2, "state": "empty", "progress": 0},
            {"meat_id": meat3, "text_id": text3, "state": "empty", "progress": 0}
        ]
        
        Ingredient(self.canvas, self, "Bun", 715, 650, "#FFCC80")
        Ingredient(self.canvas, self, "Vegetable", 795, 650, "#81C784")
        Ingredient(self.canvas, self, "tomato", 875, 650, "#EF5350")
        Ingredient(self.canvas, self, "Meat", 955, 650, "#795548", custom_cmd=lambda e: self.start_cooking_meat(e, e.x, e.y))

    def add_to_mix(self, item_name, src_x, src_y):
        zone_map = {
            "Strawberry": "Smoothies", "Orange": "Smoothies", "Ice cube": "Smoothies", "Syrup": "Smoothies",
            "Coffee Powder": "Coffee", "Cup": "Coffee", "Milk": "Coffee", "Water": "Coffee",
            "Bun": "Burger", "Vegetable": "Burger", "tomato": "Burger", "Meat": "Burger"
        }
        zone = zone_map.get(item_name)
        if not zone: return False

        if zone == "Smoothies":
            for blender in self.blenders:
                if blender["state"] in ["empty", "building"]:
                    test_mix = blender["mix"] + [item_name]
                    if self.controller.order_manager.is_valid_prefix(test_mix, zone):
                        blender["mix"].append(item_name)
                        blender["state"] = "building"
                        
                        recipe = self.controller.order_manager.identify_recipe(blender["mix"], zone)
                        if recipe:
                            blender["state"] = "blending"
                            blender["recipe_name"] = recipe
                            blender["progress"] = 0
                            self.canvas.itemconfig(blender["bg_id"], fill="#FFCDD2") 
                            self.canvas.itemconfig(blender["text_id"], text="0%", state="normal")
                            self.blend_smoothie_step(blender)
                        else:
                            self.canvas.itemconfig(blender["bg_id"], fill="#FFF59D")
                            self.canvas.itemconfig(blender["text_id"], text="\n".join(blender["mix"]), state="normal")
                        return True
            self.show_feedback(src_x, src_y, "⚠️ FULL!", "red")
            return False

        zone_slots = [slot for slot in self.holding_slots if slot.zone == zone]

        for slot in zone_slots:
            if slot.state in ["building", "ready"]:
                test_mix = slot.mix + [item_name]
                if self.controller.order_manager.is_valid_prefix(test_mix, zone):
                    slot.add_item(item_name)
                    return True 

        for slot in zone_slots:
            if slot.state == "empty":
                slot.add_item(item_name)
                return True 

        self.show_feedback(src_x, src_y, "⚠️ FULL!", "red")
        return False

    def blend_smoothie_step(self, blender):
        if not getattr(self, 'is_playing', False) or blender["state"] != "blending": return
        if getattr(self, 'is_paused', False):
            self.after(500, lambda: self.blend_smoothie_step(blender))
            return
        
        blender["progress"] += 20
        if blender["progress"] >= 100:
            blender["state"] = "ready"
            self.canvas.itemconfig(blender["bg_id"], fill="#A5D6A7") 
            self.canvas.itemconfig(blender["text_id"], text="PICK")
        else:
            self.canvas.itemconfig(blender["text_id"], text=f"{blender['progress']}%")
            self.after(500, lambda: self.blend_smoothie_step(blender))

    def pickup_blended_smoothie(self, blender, event):
        if blender["state"] == "ready":
            zone_slots = [s for s in self.holding_slots if s.zone == "Smoothies" and s.state == "empty"]
            if zone_slots:
                slot = zone_slots[0]
                slot.add_prebuilt_item(blender["recipe_name"])
                blender["mix"] = []
                blender["state"] = "empty"
                blender["recipe_name"] = None
                blender["progress"] = 0
                self.canvas.itemconfig(blender["bg_id"], fill="#CFD8DC")
                self.canvas.itemconfig(blender["text_id"], state="hidden")
            else:
                self.show_feedback(event.x, event.y, "⚠️ FULL!", "red")

    def start_cooking_meat(self, event, src_x, src_y):
        for grill in self.grills:
            if grill["state"] == "empty":
                grill["state"] = "cooking"
                grill["progress"] = 0
                self.canvas.itemconfig(grill["meat_id"], state="normal", fill="#E57373") 
                self.canvas.itemconfig(grill["text_id"], state="normal", text="0%")
                self.cook_meat_step(grill)
                return
        self.show_feedback(src_x, src_y, "⚠️ FULL!", "red")

    def cook_meat_step(self, grill):
        if not getattr(self, 'is_playing', False) or grill["state"] != "cooking": return 
        if getattr(self, 'is_paused', False):
            self.after(500, lambda: self.cook_meat_step(grill))
            return
            
        grill["progress"] += 10
        if grill["progress"] >= 100:
            grill["state"] = "cooked"
            self.canvas.itemconfig(grill["meat_id"], fill="#4E342E") 
            self.canvas.itemconfig(grill["text_id"], text="PICK")
            self.canvas.tag_bind(grill["meat_id"], "<Button-1>", lambda e, g=grill: self.pickup_cooked_meat(g, e))
            self.canvas.tag_bind(grill["text_id"], "<Button-1>", lambda e, g=grill: self.pickup_cooked_meat(g, e))
        else:
            self.canvas.itemconfig(grill["text_id"], text=f"{grill['progress']}%")
            self.after(500, lambda: self.cook_meat_step(grill))

    def pickup_cooked_meat(self, grill, event):
        if grill["state"] == "cooked":
            success = self.add_to_mix("Meat", event.x, event.y)
            if success:
                self.canvas.itemconfig(grill["meat_id"], state="hidden")
                self.canvas.itemconfig(grill["text_id"], state="hidden")
                grill["state"] = "empty"
                self.canvas.tag_unbind(grill["meat_id"], "<Button-1>")
                self.canvas.tag_unbind(grill["text_id"], "<Button-1>")

    def reset_stations(self):
        for grill in self.grills:
            self.canvas.itemconfig(grill["meat_id"], state="hidden")
            self.canvas.itemconfig(grill["text_id"], state="hidden")
            grill["state"] = "empty"
            self.canvas.tag_unbind(grill["meat_id"], "<Button-1>")
            self.canvas.tag_unbind(grill["text_id"], "<Button-1>")
            
        for blender in self.blenders:
            blender["state"] = "empty"
            blender["mix"] = []
            blender["recipe_name"] = None
            blender["progress"] = 0
            self.canvas.itemconfig(blender["bg_id"], fill="#CFD8DC")
            self.canvas.itemconfig(blender["text_id"], state="hidden")

    def on_resize(self, event):
        w_scale = event.width / self.base_w
        h_scale = event.height / self.base_h
        self.canvas.scale("all", 0, 0, w_scale, h_scale)
        
        for c in self.customer_slots:
            if c:
                c.x *= w_scale
                c.target_x *= w_scale
                c.y *= h_scale
                c.speed *= w_scale
                
        self.base_w, self.base_h = event.width, event.height
        self.scale_x = event.width / 1000.0
        self.scale_y = event.height / 750.0

    def update_timer(self):
        if not self.is_playing: return
        if self.is_paused:
            self.timer_id = self.after(1000, self.update_timer)
            return
            
        self.time_left -= 1
        mins, secs = divmod(self.time_left, 60)
        self.canvas.itemconfig(self.timer_text, text=f"TIME: {mins:02d}:{secs:02d}")
        
        if self.time_left <= 0:
            self.end_day()
        else:
            self.timer_id = self.after(1000, self.update_timer)

    def end_day(self):
        self.is_playing = False
        if self.after_id: self.after_cancel(self.after_id)
        if self.timer_id: self.after_cancel(self.timer_id)
        
        for i, c in enumerate(self.customer_slots):
            if c: c.clear(); self.customer_slots[i] = None

        popup = tk.Toplevel(self)
        popup.title(f"End of Day {self.controller.current_day}")
        
        root_x = self.controller.winfo_x()
        root_y = self.controller.winfo_y()
        root_w = self.controller.winfo_width()
        root_h = self.controller.winfo_height()
        
        pop_w, pop_h = 400, 350
        pos_x = root_x + (root_w // 2) - (pop_w // 2)
        pos_y = root_y + (root_h // 2) - (pop_h // 2)
        
        popup.geometry(f"{pop_w}x{pop_h}+{pos_x}+{pos_y}")
        popup.configure(bg="#E0F7FA")
        popup.transient(self.controller)
        popup.grab_set()

        tk.Label(popup, text=f"🌙 DAY {self.controller.current_day} FINISHED!", font=("Arial", 20, "bold"), bg="#E0F7FA", fg="#00695C").pack(pady=20)
        tk.Label(popup, text=f"💰 Cash Earned Today: ${self.daily_earned}", font=("Arial", 16), bg="#E0F7FA", fg="black").pack(pady=5)
        tk.Label(popup, text=f"✅ Successful Orders: {self.daily_success}", font=("Arial", 14), bg="#E0F7FA", fg="green").pack(pady=5)
        tk.Label(popup, text=f"❌ Failed/Angry: {self.daily_fail}", font=("Arial", 14), bg="#E0F7FA", fg="red").pack(pady=5)

        def next_day():
            self.controller.current_day += 1
            popup.destroy()
            self.start_game()

        def go_menu():
            popup.destroy()
            self.stop_game()

        tk.Button(popup, text="▶ NEXT DAY", font=("Arial", 14, "bold"), bg="#4CAF50", fg="black", width=15, command=next_day).pack(pady=15)
        tk.Button(popup, text="⬅ MAIN MENU", font=("Arial", 12), fg="black", command=go_menu).pack(pady=5)

    def start_game(self):
        if not self.is_playing:
            self.is_playing = True
            
            self.cash = 0
            self.update_cash(0)
            
            self.time_left = 120
            self.daily_earned = 0
            self.daily_success = 0
            self.daily_fail = 0
            
            self.canvas.itemconfig(self.day_text, text=f"DAY: {self.controller.current_day}")
            self.canvas.itemconfig(self.timer_text, text="TIME: 02:00")
            
            self.reset_stations()
            for slot in self.holding_slots: slot.clear()
            
            self.update_timer()
            self.spawn_customer()
            self.game_loop()

    def stop_game(self):
        self.is_playing = False
        if self.after_id: self.after_cancel(self.after_id)
        if self.timer_id: self.after_cancel(self.timer_id)
        self.reset_stations()
        for i, c in enumerate(self.customer_slots):
            if c: c.clear(); self.customer_slots[i] = None
        self.controller.show_frame("MainMenuFrame")

    def toggle_pause(self):
        if not self.is_playing: return
        self.is_paused = not self.is_paused
        if self.is_paused: self.btn_pause.config(text="▶ RESUME", fg="blue")
        else: self.btn_pause.config(text="⏸ PAUSE", fg="black")

    def show_recipes(self):
         was_paused = getattr(self, 'is_paused', False)
         if not was_paused: self.toggle_pause()
         
         popup = tk.Toplevel(self)
         popup.title("Recipes")
         popup.geometry("450x250") 
         popup.configure(bg="#FAFAFA")
         tk.Label(popup, text="📖 RECIPES INFO", font=("Arial", 14, "bold"), bg="#FAFAFA", fg="black").pack(pady=10)
         
         recipes_text = (
             "☕ Espresso ($10) = Coffee Powder + Water + Cup\n"
             "🥛 Latte ($12) = Coffee Powder + Water + Milk + Cup\n"
             "🍓 Strawberry Smoothie ($15) = Strawberry + Ice cube + Syrup\n"
             "🍊 Orange Smoothie ($15) = Orange + Ice cube + Syrup\n"
             "🍔 Burger ($20) = Bun + Vegetable + tomato + Meat"
         )
         tk.Label(popup, text=recipes_text, font=("Arial", 11), bg="#FAFAFA", fg="black", justify="left").pack(pady=5)
         def close_popup():
             if not was_paused and self.is_paused: self.toggle_pause()
             popup.destroy()
         popup.protocol("WM_DELETE_WINDOW", close_popup)
         tk.Button(popup, text="CLOSE", fg="black", command=close_popup).pack(pady=10)

    def spawn_customer(self):
        if not self.is_playing: return
        if getattr(self, 'is_paused', False):
            self.after_id = self.after(1000, self.spawn_customer)
            return
        empty = [i for i, s in enumerate(self.customer_slots) if s is None]
        if empty:
            idx = random.choice(empty)
            target_x = 166 + (idx * 333)
            self.customer_slots[idx] = Customer(self.canvas, self, target_x, 220, idx)
        self.after_id = self.after(random.randint(4000, 7000), self.spawn_customer)

    def game_loop(self):
        if not self.is_playing: return
        if getattr(self, 'is_paused', False):
            self.after(16, self.game_loop)
            return
            
        for i, c in enumerate(self.customer_slots):
            if c:
                c.update(self.controller.current_difficulty)
                if c.patience <= 0:
                    self.controller.stats_manager.log_event(c.cust_type, c.menu_id, 0, "Angry_Left", 0)
                    self.daily_fail += 1 
                    c.clear(); self.customer_slots[i] = None
                    
        self.after(16, self.game_loop)

    def start_dragging(self, event, source):
        if getattr(self, 'is_paused', False): return
        if source.state not in ["ready", "locked"]: return 
        
        self.is_dragging = True
        self.drag_source = source
        self.ghost_bg = self.canvas.create_rectangle(event.x-40, event.y-20, event.x+40, event.y+20, fill="#4CAF50", outline="black", width=2)
        self.ghost_text = self.canvas.create_text(event.x, event.y, text=source.recipe_name.replace(" ", "\n"), font=("Arial", 9, "bold"), fill="white")

    def on_drag_motion(self, event):
        if getattr(self, 'is_dragging', False):
            self.canvas.coords(self.ghost_bg, event.x-40, event.y-20, event.x+40, event.y+20)
            self.canvas.coords(self.ghost_text, event.x, event.y)

    def on_drag_release(self, event):
        if not getattr(self, 'is_dragging', False): return
        self.is_dragging = False
        self.canvas.delete(self.ghost_bg)
        self.canvas.delete(self.ghost_text)
        
        trash_coords = self.canvas.coords(self.trash_box)
        if trash_coords and (trash_coords[0] <= event.x <= trash_coords[2]) and (trash_coords[1] <= event.y <= trash_coords[3]):
            self.drag_source.clear()
            self.show_feedback(event.x, event.y, "🗑️ Trashed", "red")
            return

        target_cust = None
        for c in self.customer_slots:
            if c:
                coords = self.canvas.coords(c.id) 
                if coords and (coords[0] - 60 <= event.x <= coords[2] + 60) and (coords[1] - 100 <= event.y <= coords[3] + 80):
                    target_cust = c
                    break 
        
        if target_cust:
            is_ok = (self.drag_source.recipe_name == target_cust.menu_id)
            
            if is_ok:
                base_price = self.controller.order_manager.prices.get(target_cust.menu_id, 0)
                diff = self.controller.current_difficulty
                multiplier = 0.5 if diff == "Easy" else 2.0 if diff == "Hard" else 1.0
                earned = int(base_price * multiplier)
                
                self.daily_earned += earned
                self.daily_success += 1
            else:
                earned = 0
                self.daily_fail += 1
            
            self.controller.stats_manager.log_event(target_cust.cust_type, target_cust.menu_id, 0, "Success" if is_ok else "Fail", earned)
            
            if is_ok:
                self.update_cash(earned)
                self.show_feedback(event.x, event.y, f"✅ +${earned}", "green")
                target_cust.clear() 
                self.customer_slots[target_cust.slot_idx] = None
                self.drag_source.clear() 
            else:
                self.show_feedback(event.x, event.y, "❌ WRONG!", "red")

    def show_feedback(self, x, y, text, color):
        lbl = self.canvas.create_text(x, y, text=text, font=("Arial", 16, "bold"), fill=color, tags="all")
        def float_up(count):
            if count > 0:
                self.canvas.move(lbl, 0, -3)
                self.after(16, lambda: float_up(count - 1))
            else:
                self.canvas.delete(lbl)
        float_up(30)

class DifficultyFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFE082")
        self.controller = controller
        tk.Label(self, text="⚙ SELECT DIFFICULTY", font=("Arial", 28, "bold"), bg="#FFE082", fg="black").pack(pady=40)
        self.status_label = tk.Label(self, text=f"CURRENT: {self.controller.current_difficulty.upper()}", font=("Arial", 16, "bold"), bg="#FFE082", fg="#E65100")
        self.status_label.pack(pady=10)
        self.buttons = {}
        for d in ["Easy", "Normal", "Hard"]:
            btn = tk.Label(self, text=d.upper(), font=("Arial", 16, "bold"), width=15, pady=10, cursor="hand2", relief="raised", bd=2)
            btn.pack(pady=10)
            btn.bind("<Button-1>", lambda e, v=d: self.change_difficulty(v))
            self.buttons[d] = btn
        tk.Button(self, text="⬅ BACK TO MENU", font=("Arial", 12, "bold"), fg="black", command=lambda: controller.show_frame("MainMenuFrame")).pack(pady=40)
        self.update_button_colors()

    def change_difficulty(self, diff):
        self.controller.current_difficulty = diff 
        self.status_label.config(text=f"CURRENT: {diff.upper()}")
        self.update_button_colors() 

    def update_button_colors(self):
        for name, btn in self.buttons.items():
            if name == self.controller.current_difficulty:
                btn.config(bg="#4CAF50", fg="white") 
            else:
                btn.config(bg="white", fg="black")

class StatsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#BBDEFB")
        self.controller = controller
        tk.Label(self, text="📊 GAME STATISTICS", font=("Arial", 28, "bold"), bg="#BBDEFB", fg="black").pack(pady=20)
        
        self.tree = ttk.Treeview(self, columns=("Menu", "Status", "Earned"), show="headings")
        for c in ["Menu", "Status", "Earned"]: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=20)

        btn_fm = tk.Frame(self, bg="#BBDEFB")
        btn_fm.pack(pady=20)
        tk.Button(btn_fm, text="📈 VIEW CHARTS", font=("Arial", 12, "bold"), fg="black", command=self.controller.stats_manager.show_charts).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_fm, text="🔄 RESET ALL", font=("Arial", 12, "bold"), fg="black", command=self.reset).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_fm, text="BACK", font=("Arial", 12), fg="black", command=lambda: self.controller.show_frame("MainMenuFrame")).pack(side=tk.LEFT, padx=10)

    def update_stats(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for r in self.controller.stats_manager.records:
            self.tree.insert("", "end", values=(r["Menu"], r["Status"], r["Earned"]))

    def reset(self):
        self.controller.stats_manager.reset_stats()
        self.update_stats()