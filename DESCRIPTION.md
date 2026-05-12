# Project Description

## 1. Project Overview
**Project Name:** COFFEE RUSH TYCOON  
**Brief Description:** COFFEE RUSH TYCOON is an engaging time-management and cooking simulation game developed in Python utilizing the Tkinter GUI framework. Players assume the role of a store manager who must swiftly prepare customizable orders—ranging from custom progressive burgers to brewed coffees and blended smoothies—to satisfy incoming customers before their patience runs out entirely.

The application integrates sophisticated gameplay mechanics, including real-time progressive ingredient stacking visuals, dynamic order prefix validations, and comprehensive backend statistical tracking. Every served order, validation failure, and customer walkout is persistently logged to enable detailed business intelligence evaluations.

**Problem Statement:** Operating a fast-paced cafe environment requires sharp multi-tasking, active working memory, and quick decision-making under strict time pressure. Many existing simulation games lack integrated, real-time performance analytics that allow players to systematically evaluate their precision accuracy, popular items, and financial revenue trends.

**Target Users:** Simulation and tycoon game enthusiasts, casual players looking for engaging time-management challenges, and users interested in operational data visualization dashboards.

**Key Features:** * **Three Interactive Prep Zones:** Dedicated stations for Smoothie blending, Coffee brewing, and Burger grilling.
* **Progressive Visual Stacking:** Dynamic pixel art integration that updates progressive assembly states step-by-step as ingredients are combined.
* **Secure Pause Cover System:** A solid topmost overlay that entirely hides the game board during pauses to prevent cheating while completely blocking underlying clicks.
* **VIP Customer System:** A 25% chance to spawn special VIP customers who reward double revenue multipliers upon successful order fulfillment.
* **Integrated Data Analytics:** Real-time logging of operational metrics coupled with interactive Matplotlib visualization charts.

**Screenshots:**
<img width="1992" height="1540" alt="image" src="https://github.com/user-attachments/assets/319d8ea9-ea28-4ef0-9728-5742d28bee05" />

* ![Data Visualization]
  <img width="2190" height="864" alt="image" src="https://github.com/user-attachments/assets/41fe7dbc-40a6-459b-b51a-bb5376a0bee4" />


**Proposal:** [Download Project Proposal PDF](https://github.com/user-attachments/files/27571691/Programming.2.Proposal.6710545857.pdf)


**YouTube Presentation:** [Watch Video Presentation](https://youtu.be/SGDT1ZrRXZ8)  
*(Includes Introduction & Demo, OOP Design Explanation, and Statistical Data Visualization)*

## 2. Concept
### 2.1 Background
The fast-paced food and beverage industry serves as a rigorous environment for testing human multi-tasking and operational efficiency. Inspired by classic arcade cooking simulations, this project elevates standard gameplay by implementing highly structured Object-Oriented Programming (OOP) architectures. Furthermore, integrating a backend data analytics module emphasizes the critical importance of business intelligence and performance review in real-world store management.

### 2.2 Objectives
* To build a bug-free, highly responsive GUI cooking simulation game using Python and Tkinter.
* To apply robust OOP principles (Encapsulation, Inheritance, Association) for seamless management of complex game entities.
* To collect, store, and visualize meaningful gameplay statistics to help users evaluate their operational success rates and revenue trends.

## 3. UML Class Diagram
The UML Class Diagram illustrates the structural architecture of the system, including core classes, attributes, methods, and relationships (association, inheritance).  
**Submission Requirement:** Attach the UML Class Diagram in **.pdf format** [Download UML Class Diagram PDF](https://github.com/user-attachments/files/27639598/Coffee.Rush.Tycoon.UML.May.12.2026.pdf)

## 4. Object-Oriented Programming Implementation
Below is the complete list of classes implemented in the project along with their roles and responsibilities:

* **`CoffeeTycoonApp` (Inherits `tk.Tk`):** The main root application class responsible for window configuration, central cache preloading, controller initialization, and switching active display frames.
* **`MainMenuFrame` (Inherits `tk.Frame`):** Renders the landing dashboard, dynamic backgrounds, and navigation triggers, including the comprehensive progress reset functionality.
* **`GameFrame` (Inherits `tk.Frame`):** The primary gameplay controller holding the interactive canvas, layout HUDs, active station timers, interactive prep zones, solid pause overlays, and drag-and-serve mechanics.
* **`DifficultyFrame` (Inherits `tk.Frame`):** Provides a UI for players to dynamically toggle game difficulty (Easy, Normal, Hard) affecting patience decay multipliers.
* **`StatsFrame` (Inherits `tk.Frame`):** Renders the historical data logs via a Treeview table and provides execution triggers for generating Matplotlib charts.
* **`HoldingSlot`:** Encapsulates the mixing slots on the prep board. Independently manages its progressive state (`empty`, `building`, `ready`) and updates pixel art representations dynamically.
* **`Ingredient`:** Represents raw interactive ingredient buttons. Renders distinct background frames and item icons while handling input click triggers.
* **`Customer`:** Manages dynamic customer spawns, horizontal movement, dynamic patience decay logic, 25% VIP probability, order rendering, and UI progress bars.
* **`OrderManager`:** A robust backend engine encapsulating defined menu recipes, progressive prefix validation checks, and price mapping dictionaries.
* **`StatsManager`:** Handles persistent data logging to CSV storage, event tracking (`Success`, `Fail`, `Angry_Left`), and constructs multi-axis performance charts using Matplotlib.

## 5. Statistical Data
### 5.1 Data Recording Method
Data is recorded in real-time inside the `StatsManager` class. Whenever an order resolves (successfully served, incorrectly submitted, or the customer leaves angry due to timeout), the system appends the exact menu type, status outcome, and earned revenue into an in-memory record list. This record list is persistently exported to a local `stats.csv` file automatically.

### 5.2 Data Features
The collected dataset features categorical variables (`Menu Type`, `Status Outcome`) and numerical variables (`Earned Revenue`). These features allow direct analytical evaluation of player accuracy rates, peak profitable items, and common failure points.

## 6. Changed Proposed Features (Optional)
* **Secure Solid Pause Overlay:** Replaced standard semi-transparent overlays with a solid topmost overlay during game pauses. This entirely prevents players from cheating by inspecting the board while paused and fully secures underlying hitboxes.
* **Integrated VIP Multipliers:** Added a 25% dynamic chance for customers to spawn as VIPs, doubling the revenue earned upon correct fulfillment.

## 7. External Sources
* **GUI Framework:** Standard Python Tkinter library.
* **Image Processing:** Pillow (PIL) library for handling and resizing pixel art sprites.
* **Data Visualization:** Matplotlib library for rendering analytical multi-axis charts.
* **Artwork & Assets:** Custom pixel art assets created and structured specifically for the application.
