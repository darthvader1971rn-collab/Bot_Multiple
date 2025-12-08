import os
import json

def create_structure():
    # Definicja struktury folderów i plików
    # Klucz to ścieżka folderu -> Wartość to lista plików w tym folderze
    structure = {
        ".": [
            "main.py",
            "settings.py",           # Tu wkleisz settings.py z Bota 1
            "settings_video.json",   # Tu wkleisz/zostawisz settings.json z Bota 2
            "miasta - USA.txt",
            "miasta - Europa_Afryka.txt"
        ],
        "modules": [
            "__init__.py",
            "sequence.py",           # Tu wkleisz sequence.py (zmodyfikowany pod reklamy)
            "video_watcher.py"       # Tu wkleisz nowy moduł wideo
        ],
        # GŁÓWNA ZMIANA: Struktura grafik dla EN z rozdzielczościami
        # Bot szuka plików w formacie: resources/img/JĘZYK/SZERxWYS/
        "resources/img/en/3840x2160": [], # 4K
        "resources/img/en/2560x1440": [], # 2K (QHD)
        "resources/img/en/1920x1080": []  # FHD
    }

    print("--- Rozpoczynam tworzenie struktury projektu (Wersja EN + Multi-Res) ---")

    for folder, files in structure.items():
        # 1. Tworzenie folderu (tworzy też foldery nadrzędne, np. resources/img/en...)
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"[FOLDER] OK: {folder}")
        except OSError as e:
            print(f"[BŁĄD] Nie można utworzyć folderu {folder}: {e}")
            continue

        # 2. Tworzenie plików
        for filename in files:
            filepath = os.path.join(folder, filename)
            
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    # Puste pliki JSON muszą mieć nawiasy klamrowe
                    if filename.endswith(".json"):
                        f.write("{}") 
                    # __init__ może być pusty
                    elif filename == "__init__.py":
                        pass
                    # Reszta z komentarzem
                    else:
                        f.write(f"# TU WKLEJ KOD PLIKU: {filename}\n")
                print(f"  [PLIK] Utworzono: {filepath}")
            else:
                print(f"  [PLIK] Już istnieje: {filepath}")

    print("\n--- Zakończono! ---")
    print("1. Otwórz utworzone pliki .py i wklej kod.")
    print("2. Skopiuj swoje obrazki (.png) do odpowiedniego folderu rozdzielczości w resources/img/en/...")

if __name__ == "__main__":
    create_structure()
    input("\nNaciśnij ENTER, aby zamknąć...")
    