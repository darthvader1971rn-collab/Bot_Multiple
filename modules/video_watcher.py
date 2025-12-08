# -*- coding: utf-8 -*-
import pyautogui
import time
import random
import os
import logging
import csv
import math
import pytesseract
from PIL import Image, ImageOps
from datetime import datetime, timedelta
import settings

# Konfiguracja Tesseracta
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH

CONFIDENCE = 90.0

# --- PAMIĘĆ TYMCZASOWA (BLACKLIST) ---
BLOCKED_PLAYERS = {}

def random_time(start, end):
    return random.uniform(start, end)

def park_mouse_left_edge():
    screen_w, screen_h = pyautogui.size()
    target_y = screen_h // 2
    pyautogui.moveTo(5, target_y, duration=0.5)

def load_region(path):
    if not os.path.exists(path): return None
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            row = next(reader)
            return (int(row["LewyGorny_X"]), int(row["LewyGorny_Y"]), int(row["Szerokosc"]), int(row["Wysokosc"]))
    except: return None

def check_exists(image_name, region=None):
    full_path = os.path.join(settings.GRAPHICS_PATH, image_name)
    if not os.path.exists(full_path): return False
    try:
        return pyautogui.locateOnScreen(full_path, region=region, confidence=CONFIDENCE, grayscale=True) is not None
    except: return False

def find_and_click_simple(image_name, retry=2, wait_after=1):
    full_path = os.path.join(settings.GRAPHICS_PATH, image_name)
    if not os.path.exists(full_path): return False
    for _ in range(retry):
        try:
            loc = pyautogui.locateCenterOnScreen(full_path, confidence=CONFIDENCE, grayscale=True)
            if loc:
                logging.info(f"[VIDEO] Klikam: {image_name}")
                pyautogui.moveTo(loc)
                pyautogui.click(loc)
                time.sleep(wait_after)
                return True
        except: pass
        time.sleep(0.5)
    return False

# --- SMART LOGIC ---

def get_player_name(button_center, limit_region=None):
    bx, by = button_center
    
    # Dynamiczne wymiary z settings
    off_x = getattr(settings, 'OCR_OFFSET_X', 185)
    off_y = getattr(settings, 'OCR_OFFSET_Y', 85)
    width = getattr(settings, 'OCR_WIDTH', 355)
    height = getattr(settings, 'OCR_HEIGHT', 55)
    
    region_x = int(bx - off_x)
    region_y = int(by - off_y)
    
    # Clamping
    if limit_region:
        limit_x, limit_y, limit_w, limit_h = limit_region
        if region_x < limit_x: region_x = limit_x

    try:
        screenshot = pyautogui.screenshot(region=(region_x, region_y, width, height))
        gray = ImageOps.grayscale(screenshot)
        bw = gray.point(lambda p: 255 if p > 180 else 0)
        text = pytesseract.image_to_string(bw, config="--psm 7").strip()
        clean_name = "".join(e for e in text if e.isalnum())
        return clean_name
    except Exception:
        return ""

def find_and_click_smart_dollar(image_name, region=None):
    full_path = os.path.join(settings.GRAPHICS_PATH, image_name)
    if not os.path.exists(full_path): return False

    try:
        # Grayscale=False dla fioletowych dolarów
        is_gray = True
        if "purple" in image_name: is_gray = False
            
        candidates = list(pyautogui.locateAllOnScreen(full_path, region=region, confidence=CONFIDENCE, grayscale=is_gray))
        
        # Fallback na cały ekran
        if not candidates and region is not None:
             candidates = list(pyautogui.locateAllOnScreen(full_path, confidence=CONFIDENCE, grayscale=is_gray))

        if not candidates: return False
        
        candidates.sort(key=lambda b: (b.top, b.left))

        logging.info(f"[SMART] Widzę {len(candidates)} dolarów '{image_name}'.")

        for box in candidates:
            cx = box.left + box.width // 2
            cy = box.top + box.height // 2
            
            # 1. Odczytaj nick
            player_name = get_player_name((cx, cy), limit_region=region)
            
            # Jeśli nick pusty, uznajemy go za "Unknown" i klikamy (zamiast pomijać)
            if not player_name:
                player_name = "Unknown_Player"

            # 2. Sprawdź Blacklistę
            if player_name in BLOCKED_PLAYERS:
                unban_time = BLOCKED_PLAYERS[player_name]
                if datetime.now() > unban_time:
                    logging.info(f"[SMART] Ban dla '{player_name}' wygasł.")
                    del BLOCKED_PLAYERS[player_name]
                else:
                    logging.info(f"[SMART] Gracz '{player_name}' zbanowany. Pomijam.")
                    continue 
            
            # 3. Kliknij
            logging.info(f"[VIDEO] Klikam dolara u gracza: '{player_name}'")
            pyautogui.moveTo(cx, cy)
            pyautogui.click(cx, cy)
            time.sleep(2.5) 
            
            # 4. Limit Check (Czy wyskoczyło okienko limitu?)
            if check_exists("account_limit.png"):
                logging.warning(f"[LIMIT] Pełne konto u gracza: {player_name}!")
                
                if player_name != "Unknown_Player":
                    unban_time = datetime.now() + timedelta(hours=2)
                    BLOCKED_PLAYERS[player_name] = unban_time
                    logging.info(f"[BLACKLIST] Zbanowano gracza do {unban_time.strftime('%H:%M')}")
                
                time.sleep(1)
                find_and_click_simple("close_account_limit.png", retry=4, wait_after=1)
                
                continue # Idź do następnego kandydata
            
            return True # Sukces (kliknięto i nie było błędu)
            
    except Exception:
        pass
        
    return False

def wait_for_button(target_image, max_seconds=65, check_interval=5):
    logging.info(f"[VIDEO] Czekam na {target_image} (Max {max_seconds}s)...")
    park_mouse_left_edge()
    start_time = time.time()
    while time.time() - start_time < max_seconds:
        if check_exists(target_image, region=None):
            logging.info(f"[VIDEO] Wykryto: {target_image}!")
            return True
        time.sleep(check_interval)
    logging.warning(f"[VIDEO] Timeout! Nie znaleziono {target_image}.")
    return False

# --- GŁÓWNA PĘTLA CYKLU ---

def watch_cycle():
    logging.info("[VIDEO] --- START CYKLU (Priorytet: Bonusy -> Wideo) ---")

    bonus_region = load_region(settings.CSV_REGION_BONUS)
    
    # FAZA 1: CZYSZCZENIE PLANSZY (PRESTIŻ I DOLARY)
    # Pętla wykonuje się tak długo, jak długo znajduje jakiekolwiek bonusy do zebrania.
    # Dopiero gdy nic nie znajdzie, przechodzi do reklam.
    
    start_collection = time.time()
    while True:
        # Bezpiecznik czasowy (żeby nie utknął w pętli zbierania na zawsze)
        if time.time() - start_collection > 120: 
            logging.warning("[VIDEO] Przekroczono czas zbierania bonusów.")
            break

        collected_something = False

        # 1. Prestiż (Priorytet najwyższy)
        if find_and_click_simple("prestige_purple.png", retry=1, wait_after=2.5):
            collected_something = True
            continue # Restart pętli, szukaj kolejnych
        
        if find_and_click_simple("prestige.png", retry=1, wait_after=2.5):
            collected_something = True
            continue

        # 2. Dolary (Priorytet średni)
        if find_and_click_smart_dollar("dollar_purple.png", region=bonus_region):
            collected_something = True
            continue
            
        if find_and_click_smart_dollar("dollar.png", region=bonus_region):
            collected_something = True
            continue

        # Jeśli w tym obiegu nic nie znaleziono, przerywamy pętlę zbierania
        if not collected_something:
            break

    # FAZA 2: OGLĄDANIE REKLAM
    # Sprawdzamy, czy w ogóle jest opcja wideo
    
    video_available = False
    if check_exists("video_enabled.png") or check_exists("video_new.png") or check_exists("play_icon.png"):
        video_available = True
    
    if not video_available:
        logging.info("[VIDEO] Brak bonusów i brak wideo. Koniec.")
        return False

    # Wejście w tryb Playera (jeśli trzeba kliknąć w ikonę biletu/wideo)
    if not check_exists("play_icon.png"):
        if find_and_click_simple("video_enabled.png", retry=1, wait_after=2): pass
        elif find_and_click_simple("video_new.png", retry=1, wait_after=2): pass

    logging.info("[VIDEO] Film 1: Start.")
    if not find_and_click_simple("play_icon.png", retry=5, wait_after=0):
        logging.warning("[VIDEO] Nie widzę Play. Koniec.")
        return False

    if wait_for_button("watch_video.png", max_seconds=70):
        find_and_click_simple("watch_video.png", wait_after=2)
        
        logging.info("[VIDEO] Film 2: Start.")
        if not find_and_click_simple("play_icon.png", retry=5, wait_after=0):
             logging.warning("[VIDEO] Nie widzę Play (Film 2).")

        if wait_for_button("redeem.png", max_seconds=70):
            logging.info("[VIDEO] Odbieram nagrodę...")
            find_and_click_simple("redeem.png", retry=8, wait_after=2)
        else:
            logging.warning("[VIDEO] Nie pojawił się Redeem po 2. filmie.")
    
    else:
        # Fallback (czasem jest tylko 1 film)
        if check_exists("redeem.png"):
            logging.info("[VIDEO] Wykryto Redeem (Tylko 1 film?). Odbieram.")
            find_and_click_simple("redeem.png", retry=8, wait_after=2)
        else:
            logging.warning("[VIDEO] Cykl nieudany.")

    time.sleep(1)
    
    # Zamykanie okienek po nagrodach
    if check_exists("lottery_png.png"): find_and_click_simple("close_lottery.png", wait_after=1)
    elif check_exists("lottery.png"): find_and_click_simple("close_lottery.png", wait_after=1)

    if check_exists("pollux.png"): find_and_click_simple("close_pollux.png")
    elif check_exists("no_gold_bonus.png"): find_and_click_simple("no_gold_bonus.png")
    
    logging.info("[VIDEO] Koniec cyklu.")
    return True