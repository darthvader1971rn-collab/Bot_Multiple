import pyautogui
import pytesseract
from PIL import Image, ImageOps
import time
import os

# --- KONFIGURACJA ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# NOWE WYMIARY (Przesunięcie w górę o 25px względem poprzedniego)
OFFSET_X = -185
OFFSET_Y = -85   # Było -60, teraz -85 (wyżej)
WIDTH = 355
HEIGHT = 55

# Jeśli obrazki wychodzą czarne, zmniejsz to do 100 lub 80
THRESHOLD = 180 

def test_capture():
    print("\n--- TEST OCR v3 (Offset -85) ---")
    print("1. Najedź myszką na środek dolara.")
    print("2. Wciśnij ENTER.")
    input()
    
    mx, my = pyautogui.position()
    print(f"Mysz: {mx}, {my}")
    
    # Obliczamy region
    x = int(mx + OFFSET_X)
    y = int(my + OFFSET_Y)
    
    # Zabezpieczenie
    if x < 0: x = 0
    if y < 0: y = 0
    
    print(f"Wycinek: X={x}, Y={y}, W={WIDTH}, H={HEIGHT}")
    
    try:
        # 1. ORYGINAŁ
        img = pyautogui.screenshot(region=(x, y, WIDTH, HEIGHT))
        img.save("1_original.png")
        print("Zapisałem: 1_original.png (Sprawdź czy widać nick!)")
        
        # 2. SZAROŚĆ
        gray = ImageOps.grayscale(img)
        gray.save("2_gray.png")
        
        # 3. PROGOWANIE (Czern i Biel)
        bw = gray.point(lambda p: 255 if p > THRESHOLD else 0)
        bw.save("3_threshold.png")
        print(f"Zapisałem: 3_threshold.png")
        
        # 4. OCR
        text = pytesseract.image_to_string(bw, config="--psm 7").strip()
        print(f"\n>>> WYNIK OCR: '{text}' <<<\n")
        
        # Test czyszczenia
        clean = "".join(e for e in text if e.isalnum())
        print(f"Nick po czyszczeniu: '{clean}'")
        
    except Exception as e:
        print(f"BŁĄD: {e}")

if __name__ == "__main__":
    while True:
        test_capture()
        print("Enter = Ponów, Ctrl+C = Koniec")