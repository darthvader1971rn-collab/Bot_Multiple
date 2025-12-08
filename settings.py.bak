# -*- coding: utf-8 -*-
import os
import pyautogui
import logging

# --- KONFIGURACJA GRACZA ---
PLAYER_NICK = "DarthVader1971"  # Twój nick w grze
CONTEST_TIMEOUT = 1200     # Czas trwania konkursu w sekundach (bezpiecznik)

# --- DETEKCJA ROZDZIELCZOŚCI I SKALOWANIE ---
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
RESOLUTION_STRING = f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"

# Bazowe wymiary OCR dla 4K (Wzorzec)
BASE_WIDTH_4K = 3840
BASE_OFFSET_X = 185
BASE_OFFSET_Y = 85
BASE_OCR_W = 355
BASE_OCR_H = 55

# Obliczamy współczynnik skalowania
scale_factor = SCREEN_WIDTH / BASE_WIDTH_4K

# Wyliczamy dynamiczne wartości dla obecnego ekranu
OCR_OFFSET_X = int(BASE_OFFSET_X * scale_factor)
OCR_OFFSET_Y = int(BASE_OFFSET_Y * scale_factor)
OCR_WIDTH = int(BASE_OCR_W * scale_factor)
OCR_HEIGHT = int(BASE_OCR_H * scale_factor)

# --- WYBÓR FOLDERU KONFIGURACYJNEGO ---
if SCREEN_WIDTH == 3840:
    CONFIG_FOLDER_NAME = "config_4k"
elif SCREEN_WIDTH == 2560:
    CONFIG_FOLDER_NAME = "config_2k"
elif SCREEN_WIDTH <= 1920:
    CONFIG_FOLDER_NAME = "config_laptop"
else:
    CONFIG_FOLDER_NAME = "config_laptop"
    logging.warning(f"Nierozpoznana rozdzielczość {RESOLUTION_STRING}. Używam config_laptop.")

# --- BUDOWANIE ŚCIEŻEK ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Ścieżka do plików CSV (Regionów)
CONFIG_PATH = os.path.join(BASE_DIR, CONFIG_FOLDER_NAME)

# 2. Ścieżka do grafik (resources/img/en/ROZDZIELCZOŚĆ)
GRAPHICS_PATH = os.path.join(BASE_DIR, "resources", "img", "en", RESOLUTION_STRING)

# 3. Ścieżka do screenshotów debugowania
SCREENSHOTS_PATH = os.path.join(BASE_DIR, "screenshots")

# 4. Ścieżka do Tesseracta
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print(f"[SETTINGS] Wykryto ekran: {RESOLUTION_STRING} (Skala: {scale_factor:.2f})")
print(f"[SETTINGS] Używany folder config: {CONFIG_FOLDER_NAME}")
print(f"[SETTINGS] Auto-OCR: Offset({OCR_OFFSET_X}, {OCR_OFFSET_Y}), Wymiary({OCR_WIDTH}x{OCR_HEIGHT})")

# --- LISTA MIAST ---
CITIES = [
    "Abuja", "Albuquerque", "Amarillo", "Athens", "Augusta", "Berlin", "Bismarck", "Boise", 
    "Boston", "Buffalo", "Cairo", "Casper", "Charlotte", "Chicago", "Columbus", "Dallas", 
    "Davenport", "Denver", "Detroit", "El Paso", "Eugene", "Helena", "Houston", "Indianapolis", 
    "Jacksonville", "Kansas City", "Las Vegas", "Little Rock", "Los Angeles", "Madrid", 
    "Marrakesh", "Memphis", "Miami", "Midland", "Milwaukee", "Minneapolis", "Montgomery", 
    "Nashville", "New Orleans", "New York", "Norfolk", "Oklahoma City", "Omaha", "Paris", 
    "Phoenix", "Portland", "Rapid City", "Reno", "Salt Lake City", "San Antonio", "San Diego", 
    "San Francisco", "Seattle", "St. Louis", "Stockholm", "Walla Walla", "Washington", "Wichita"
]

# --- PLIKI CSV (PEŁNE ŚCIEŻKI) ---
CSV_REGION_MAIN = os.path.join(CONFIG_PATH, "prostokat.csv") 
CSV_REGION_LISTING = os.path.join(CONFIG_PATH, "prostokat_listing.csv")
CSV_REGION_WAGONY = os.path.join(CONFIG_PATH, "prostokat_wagony.csv")
CSV_REGION_SIGN_UP = os.path.join(CONFIG_PATH, "przycisk_sign_up.csv")
CSV_REGION_POCIAGI = os.path.join(CONFIG_PATH, "prostokat_pociagi.csv")
CSV_REGION_ROZKLAD = os.path.join(CONFIG_PATH, "prostokat_rozklad.csv")
CSV_REGION_BONUS = os.path.join(CONFIG_PATH, "prostokat_bonusy.csv")