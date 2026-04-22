import os
import csv
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# ระบบจัดการสถิติ
# ==========================================
class StatsManager:
    def __init__(self):
        self.filepath = os.path.join(BASE_DIR, "stats.csv")
        self.records = self.load_stats()

    def load_stats(self):
        records = []
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        records.append({
                            "Menu": row["Menu"],
                            "Status": row["Status"],
                            "Earned": int(row["Earned"])
                        })
            except Exception as e:
                print("Load CSV Error:", e)
        return records

    def save_stats(self):
        try:
            with open(self.filepath, "w", encoding="utf-8", newline="") as f:
                fieldnames = ["Menu", "Status", "Earned"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in self.records:
                    writer.writerow(r)
        except Exception as e:
            print("Save CSV Error:", e)

    def log_event(self, cust_type, menu, time_taken, status, earned):
        self.records.append({"Menu": menu, "Status": status, "Earned": earned})
        self.save_stats()  

    def show_charts(self):
        if not self.records:
            print("ยังไม่มีข้อมูลสำหรับสร้างกราฟ!")
            return

        status_counts = {"Success": 0, "Fail": 0, "Angry_Left": 0}
        menu_earnings = {}
        menu_counts = {} 

        for r in self.records:
            status = r["Status"]
            menu = r["Menu"]
            earned = r["Earned"]

            if status in status_counts: status_counts[status] += 1
            else: status_counts[status] = 1

            if status == "Success":
                menu_earnings[menu] = menu_earnings.get(menu, 0) + earned
                
            menu_counts[menu] = menu_counts.get(menu, 0) + 1

        popup = tk.Toplevel()
        popup.title("📈 Game Statistics Charts")
        popup.geometry("1100x400")

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))

        labels = [k for k, v in status_counts.items() if v > 0]
        sizes = [v for k, v in status_counts.items() if v > 0]
        color_map = {"Success": "#4CAF50", "Fail": "#F44336", "Angry_Left": "#FF9800"}
        actual_colors = [color_map.get(l, '#999999') for l in labels]

        if sizes:
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=actual_colors)
        ax1.set_title("Order Status (Success Rate)")

        if menu_earnings:
            menus = list(menu_earnings.keys())
            earnings = list(menu_earnings.values())
            menus_short = [m.replace(" Smoothie", "\nSmoothie") for m in menus]
            
            ax2.bar(menus_short, earnings, color="#2196F3")
            ax2.set_ylabel("Revenue ($)")
        ax2.set_title("Revenue by Menu")

        if menu_counts:
            menus = list(menu_counts.keys())
            counts = list(menu_counts.values())
            menus_short = [m.replace(" Smoothie", "\nSmoothie") for m in menus]
            
            ax3.bar(menus_short, counts, color="#9C27B0")
            ax3.set_ylabel("Number of Orders")
        ax3.set_title("Popularity (Orders Count)")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def reset_stats(self):
        self.records = []
        self.save_stats()


# ==========================================
# ระบบจัดการสูตรอาหารและราคา
# ==========================================
class OrderManager:
    def __init__(self):
        self.recipes = {
            "Espresso": ["Coffee Powder", "Water", "Cup"],
            "Latte": ["Coffee Powder", "Water", "Milk", "Cup"],
            "Strawberry Smoothie": ["Strawberry", "Ice cube", "Syrup"],
            "Orange Smoothie": ["Orange", "Ice cube", "Syrup"],
            "Burger": ["Bun", "Vegetable", "tomato", "Meat"]
        }
        
        self.prices = {
            "Espresso": 10,
            "Latte": 12,
            "Strawberry Smoothie": 15,
            "Orange Smoothie": 15,
            "Burger": 20
        }
        
        self.zone_map = {
            "Smoothies": ["Strawberry Smoothie", "Orange Smoothie"],
            "Coffee": ["Espresso", "Latte"],
            "Burger": ["Burger"]
        }
        
    def get_recipes_by_zone(self, zone):
        return {k: self.recipes[k] for k in self.zone_map[zone]}

    def is_valid_prefix(self, mix, zone):
        zone_recipes = self.get_recipes_by_zone(zone)
        for name, ingredients in zone_recipes.items():
            if len(mix) <= len(ingredients) and all(mix.count(i) <= ingredients.count(i) for i in mix):
                return True
        return False

    def identify_recipe(self, mix, zone):
        zone_recipes = self.get_recipes_by_zone(zone)
        for name, ingredients in zone_recipes.items():
            if sorted(mix) == sorted(ingredients):
                return name
        return None