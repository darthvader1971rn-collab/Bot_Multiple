# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import pyautogui
import sys
import os
import settings
from modules import sequence

# Zmienna przechowująca wybraną funkcję do uruchomienia
SELECTED_FUNCTION = None
AUTO_START_TIMER = None

def setup_console_buffer():
    os.system("mode con: cols=140 lines=9000")
    os.system("title Rail Nation Bot - Console")

def get_gui_geometry():
    screen_w, screen_h = pyautogui.size()
    if screen_w == 3840: return "915x888+1437+418"
    elif screen_w == 1920 or screen_w == 1536: return "480x452+687+196"
    else: return "500x550+100+100"

def start_gui(geometry):
    global SELECTED_FUNCTION, AUTO_START_TIMER
    root = tk.Tk()
    root.title("Centrum Sterowania")
    if geometry: root.geometry(geometry)
    root.configure(bg="#2b2b2b")

    def set_bot1_mode(mode_name, img_name):
        global SELECTED_FUNCTION
        if AUTO_START_TIMER: root.after_cancel(AUTO_START_TIMER)
        print(f"[GUI] Wybrano: {mode_name}")
        sequence.set_farming_mode(img_name)
        SELECTED_FUNCTION = sequence.contest_loop
        root.destroy()

    # --- AUTOSTART ---
    countdown_seconds = 600 
    def update_countdown():
        nonlocal countdown_seconds
        countdown_seconds -= 1
        if countdown_seconds > 0:
            root.title(f"Autostart za {countdown_seconds}s...")
            global AUTO_START_TIMER
            AUTO_START_TIMER = root.after(1000, update_countdown)
        else:
            print("[GUI] Czas minął! Autostart Kalkulatora.")
            set_bot1_mode("AUTO-Kalkulator", "Timetable_calculator.png")

    AUTO_START_TIMER = root.after(1000, update_countdown)

    lbl_title = tk.Label(root, text="Wybierz tryb (Autostart za 10 min):", font=("Arial", 12, "bold"), fg="white", bg="#2b2b2b")
    lbl_title.pack(pady=15)

    btn_style = {"font": ("Arial", 11), "width": 35, "height": 1}
    
    tk.Label(root, text="--- Farming & Konkursy ---", font=("Arial", 10), fg="#aaa", bg="#2b2b2b").pack(pady=5)
    tk.Button(root, text="Farming: MAGAZYNY", command=lambda: set_bot1_mode("Magazyny", "farm_magazyny.png"), **btn_style).pack(pady=2)
    tk.Button(root, text="Farming: MIASTA", command=lambda: set_bot1_mode("Miasta", "farm_miasta.png"), **btn_style).pack(pady=2)
    tk.Button(root, text="Farming: KARIERA", command=lambda: set_bot1_mode("Kariera", "Career_engine.png"), **btn_style).pack(pady=2)
    
    tk.Button(root, text="KALKULATOR + REKLAMY", command=lambda: set_bot1_mode("Kalkulator", "Timetable_calculator.png"), **btn_style, bg="#004400", fg="white").pack(pady=10)
    
    tk.Button(root, text="START STANDARD", command=lambda: set_bot1_mode("Default", "rozklad_zapisany.png"), **btn_style, bg="#444", fg="white").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    setup_console_buffer()
    gui_geom = get_gui_geometry()
    try:
        start_gui(gui_geom)
    except Exception as e:
        print(f"[ERROR GUI] {e}")
    
    if SELECTED_FUNCTION:
        print(f"--- Uruchamianie wybranego modułu... ---")
        try: SELECTED_FUNCTION()
        except KeyboardInterrupt: print("\nZatrzymano.")
    else: print("Zamykanie.")