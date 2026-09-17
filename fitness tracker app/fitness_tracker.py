"""
Fitness Tracker App
A simple desktop app for logging daily fitness activities and viewing progress.

Built with:
  - Tkinter + ttkthemes (UI)
  - SQLite (local data storage)
  - matplotlib (weekly progress chart)

Install once:   pip install ttkthemes matplotlib
Run with:        python fitness_tracker.py
"""

import sqlite3
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

DB_FILE = "fitness_tracker.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        activity TEXT NOT NULL,
        duration INTEGER NOT NULL,
        calories INTEGER NOT NULL,
        steps INTEGER NOT NULL
    )
""")
conn.commit()

# Daily goals used for the progress bars on the dashboard
STEPS_GOAL = 10000
CALORIES_GOAL = 500

ACTIVITY_TYPES = ["Walking", "Running", "Cycling", "Gym", "Yoga", "Other"]

# ---------------------------------------------------------------------------
# Colors / fonts
# ---------------------------------------------------------------------------

ACCENT = "#2E7D32"       # green — fitness / progress
ACCENT_LIGHT = "#E8F5E9"
TEXT_MAIN = "#1B1F23"
TEXT_MUTED = "#6B7280"

FONT_TITLE = ("Arial", 24, "bold")
FONT_HEADING = ("Arial", 14, "bold")
FONT_LABEL = ("Arial", 12)
FONT_BUTTON = ("Arial", 11, "bold")

# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------

window = ThemedTk(theme="arc")
window.title("Fitness Tracker")
window.geometry("780x600")
window.minsize(700, 560)

title_label = ttk.Label(window, text="🏃 Fitness Tracker", font=FONT_TITLE)
title_label.pack(pady=(20, 10))

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))

log_tab = ttk.Frame(notebook, padding=20)
dashboard_tab = ttk.Frame(notebook, padding=20)

notebook.add(log_tab, text="  Log Activity  ")
notebook.add(dashboard_tab, text="  Dashboard  ")

# ---------------------------------------------------------------------------
# TAB 1 — Log Activity
# ---------------------------------------------------------------------------

form_frame = ttk.Frame(log_tab)
form_frame.pack(fill="x", pady=(0, 15))

ttk.Label(form_frame, text="Activity:", font=FONT_LABEL).grid(row=0, column=0, sticky="w", padx=5, pady=8)
activity_var = tk.StringVar(value=ACTIVITY_TYPES[0])
activity_combo = ttk.Combobox(form_frame, textvariable=activity_var, values=ACTIVITY_TYPES, state="readonly", width=15)
activity_combo.grid(row=0, column=1, padx=5, pady=8)

ttk.Label(form_frame, text="Duration (min):", font=FONT_LABEL).grid(row=0, column=2, sticky="w", padx=5, pady=8)
duration_entry = ttk.Entry(form_frame, width=10)
duration_entry.grid(row=0, column=3, padx=5, pady=8)

ttk.Label(form_frame, text="Calories:", font=FONT_LABEL).grid(row=1, column=0, sticky="w", padx=5, pady=8)
calories_entry = ttk.Entry(form_frame, width=10)
calories_entry.grid(row=1, column=1, padx=5, pady=8, sticky="w")

ttk.Label(form_frame, text="Steps:", font=FONT_LABEL).grid(row=1, column=2, sticky="w", padx=5, pady=8)
steps_entry = ttk.Entry(form_frame, width=10)
steps_entry.grid(row=1, column=3, padx=5, pady=8)


def add_entry():
    activity = activity_var.get()
    duration = duration_entry.get().strip()
    calories = calories_entry.get().strip()
    steps = steps_entry.get().strip()

    if not duration or not calories:
        messagebox.showwarning("Missing Info", "Please enter at least duration and calories.")
        return

    if not duration.isdigit() or not calories.isdigit() or (steps and not steps.isdigit()):
        messagebox.showwarning("Invalid Input", "Duration, calories, and steps must be numbers.")
        return

    steps = steps if steps else "0"
    today = datetime.date.today().isoformat()

    cursor.execute(
        "INSERT INTO logs (date, activity, duration, calories, steps) VALUES (?, ?, ?, ?, ?)",
        (today, activity, int(duration), int(calories), int(steps))
    )
    conn.commit()

    duration_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)
    steps_entry.delete(0, tk.END)

    refresh_log_list()
    refresh_dashboard()
    messagebox.showinfo("Saved", "Activity logged successfully!")


add_button = ttk.Button(log_tab, text="＋ Add Entry", command=add_entry)
add_button.pack(pady=(0, 15))

ttk.Label(log_tab, text="Your Logged Activities", font=FONT_HEADING).pack(anchor="w", pady=(5, 8))

columns = ("date", "activity", "duration", "calories", "steps")
log_tree = ttk.Treeview(log_tab, columns=columns, show="headings", height=10)
for col, label, width in [
    ("date", "Date", 100),
    ("activity", "Activity", 100),
    ("duration", "Duration (min)", 110),
    ("calories", "Calories", 90),
    ("steps", "Steps", 90),
]:
    log_tree.heading(col, text=label)
    log_tree.column(col, width=width, anchor="center")

log_tree.pack(fill="both", expand=True)


def delete_selected():
    selected = log_tree.selection()
    if not selected:
        messagebox.showinfo("No Selection", "Please select an entry to delete.")
        return

    confirm = messagebox.askyesno("Delete Entry", "Delete the selected activity log?")
    if confirm:
        for item in selected:
            log_id = log_tree.item(item, "tags")[0]
            cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
        conn.commit()
        refresh_log_list()
        refresh_dashboard()


delete_button = ttk.Button(log_tab, text="🗑 Delete Selected", command=delete_selected)
delete_button.pack(pady=10)


def refresh_log_list():
    for row in log_tree.get_children():
        log_tree.delete(row)

    cursor.execute("SELECT id, date, activity, duration, calories, steps FROM logs ORDER BY id DESC")
    for log_id, date, activity, duration, calories, steps in cursor.fetchall():
        log_tree.insert("", "end", values=(date, activity, duration, calories, steps), tags=(str(log_id),))


# ---------------------------------------------------------------------------
# TAB 2 — Dashboard
# ---------------------------------------------------------------------------

summary_frame = ttk.Frame(dashboard_tab)
summary_frame.pack(fill="x", pady=(0, 20))


def make_summary_card(parent, label_text):
    card = ttk.Frame(parent, padding=15, relief="groove")
    card.pack(side="left", expand=True, fill="both", padx=8)

    value_label = ttk.Label(card, text="0", font=("Arial", 22, "bold"))
    value_label.pack()

    ttk.Label(card, text=label_text, font=FONT_LABEL).pack()

    return value_label


steps_value_label = make_summary_card(summary_frame, "Steps Today")
calories_value_label = make_summary_card(summary_frame, "Calories Today")
minutes_value_label = make_summary_card(summary_frame, "Minutes Today")

# Progress bars
progress_frame = ttk.Frame(dashboard_tab)
progress_frame.pack(fill="x", pady=(0, 20))

ttk.Label(progress_frame, text=f"Steps Goal ({STEPS_GOAL})", font=FONT_LABEL).pack(anchor="w")
steps_progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate", maximum=STEPS_GOAL)
steps_progress.pack(fill="x", pady=(2, 12))

ttk.Label(progress_frame, text=f"Calories Goal ({CALORIES_GOAL})", font=FONT_LABEL).pack(anchor="w")
calories_progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate", maximum=CALORIES_GOAL)
calories_progress.pack(fill="x", pady=(2, 0))

# Weekly chart
chart_label = ttk.Label(dashboard_tab, text="Last 7 Days — Calories Burned", font=FONT_HEADING)
chart_label.pack(anchor="w", pady=(15, 8))

fig = Figure(figsize=(6.5, 2.8), dpi=90)
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.25)

chart_canvas = FigureCanvasTkAgg(fig, master=dashboard_tab)
chart_canvas.get_tk_widget().pack(fill="both", expand=True)


def refresh_dashboard():
    today = datetime.date.today().isoformat()

    cursor.execute("SELECT COALESCE(SUM(steps),0), COALESCE(SUM(calories),0), COALESCE(SUM(duration),0) "
                    "FROM logs WHERE date = ?", (today,))
    total_steps, total_calories, total_minutes = cursor.fetchone()

    steps_value_label.config(text=str(total_steps))
    calories_value_label.config(text=str(total_calories))
    minutes_value_label.config(text=str(total_minutes))

    steps_progress["value"] = min(total_steps, STEPS_GOAL)
    calories_progress["value"] = min(total_calories, CALORIES_GOAL)

    # Last 7 days chart
    days = [(datetime.date.today() - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    day_labels = [d.strftime("%a") for d in days]
    day_calories = []

    for d in days:
        cursor.execute("SELECT COALESCE(SUM(calories),0) FROM logs WHERE date = ?", (d.isoformat(),))
        day_calories.append(cursor.fetchone()[0])

    ax.clear()
    ax.bar(day_labels, day_calories, color=ACCENT)
    ax.set_ylabel("Calories")
    fig.tight_layout()
    chart_canvas.draw()


# ---------------------------------------------------------------------------
# Initial load
# ---------------------------------------------------------------------------

refresh_log_list()
refresh_dashboard()

window.mainloop()
