# COFFEE RUSH TYCOON  

## Project Description  
**Project by:** Methawat Pichitpreechapong  
**Game Genre:** Tycoon, Time Management, Cooking Simulation    

COFFEE RUSH TYCOON is an interactive cafe management game built entirely in Python. Players prepare customizable burgers, blended smoothies, and brewed coffees under strict time constraints while managing financial earnings and reviewing operational statistics.  

## Installation  

To clone this project repository:  
```sh
git clone [https://github.com/]https://github.com/Methawat-Pichitpreechapong/Coffee-Rush-Tycoon.git 
cd [your repository]
```

To create and activate the Python virtual environment:

Windows: ```bat
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt


**Mac:** 
```sh
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
```

**Running Guide**
- After activating the Python virtual environment, you can run the game using:

Windows: ```bat
python main.py


**Mac:** 
```sh
python3 main.py
```

Tutorial / Usage
1. Main Menu: Launch the app to access the main dashboard. Click START GAME to begin a shift, DIFFICULTY to adjust challenge multipliers, VIEW STATS to review historic logs, or RESET ALL PROGRESS to clear CSV records back to Day 1.

2. Preparing Orders:
- Check incoming customer request bubbles.
- Click ingredients at the bottom to assemble items progressively into mixing slots or blenders.
- For cooked meat, click the raw meat button to place it on the grill, wait for progress to reach 100%, and click to pick it up.
- For smoothies, combine fruit + ice + syrup in the blender, wait for progress completion, and click to pick up.

3. Serving & Trashing: Click and drag ready items from the holding slots directly onto the matching customer. If you make a mistake, drag the incorrect item to the TRASH bin.

4. Pause & Recipes: Use the PAUSE button to safely halt the timer (hiding the board entirely), or click RECIPES for quick ingredient guides.

**Game Features**
- Dynamic Order Stacking: Features complete progressive pixel art updates as items are assembled step-by-step.

- VIP Customers: A 25% chance for customers to spawn as VIPs, doubling the revenue earned upon successful fulfillment.

- 100% Foolproof Combinations: Pre-cached mathematical subset combinations per prep zone prevent application crashes entirely.

- Integrated Business Analytics: Displays interactive charts (Pie charts and Bar graphs) evaluating daily performance.

- Secure Pause System: Prevents board inspection during pauses via an integrated topmost cover layout.

**Known Bugs**
None. All core gameplay features, custom graphic rendering, dynamic order validations, and complete statistical tracking components have been fully implemented and tested.

**Unfinished Works**
None. The application is 100% complete.

**External Sources**
- Custom Original Pixel Art assets.

- Standard GUI Framework by Python Tkinter & Pillow.

- Statistics Charting engine powered by Matplotlib.
