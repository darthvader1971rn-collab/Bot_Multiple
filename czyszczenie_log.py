import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import os

# Zmienna globalna na ścieżkę do pliku
sciezka_pliku = ""

def wybierz_plik():
    global sciezka_pliku
    plik = filedialog.askopenfilename(
        title="Wybierz plik loga",
        filetypes=[("Pliki log", "*.log"), ("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    )
    if plik:
        sciezka_pliku = plik
        nazwa = os.path.basename(plik)
        label_plik_info.config(text=f"Wybrano: {nazwa}", foreground="green")
        info_label.config(text="") # Czyścimy komunikaty błędów

def aktualizuj_godzine(val):
    label_godzina.config(text=f"{int(float(val)):02d}")
    aktualizuj_granice()

def aktualizuj_minuta(val):
    label_minuta.config(text=f"{int(float(val)):02d}")
    aktualizuj_granice()

def aktualizuj_sekunda(val):
    label_sekunda.config(text=f"{int(float(val)):02d}")
    aktualizuj_granice()

def aktualizuj_granice():
    d = kalendarz.get_date()
    g = int(suwak_godzina.get())
    m = int(suwak_minuta.get())
    s = int(suwak_sekunda.get())
    # Wyświetlamy w formacie uniwersalnym YYYY-MM-DD
    gran_text = f"{d.strftime('%Y-%m-%d')} {g:02d}:{m:02d}:{s:02d}"
    granica_label.config(text=f"Wybrana granica: {gran_text}")

def filtruj_log():
    if not sciezka_pliku:
        messagebox.showwarning("Brak pliku", "Najpierw wybierz plik loga przyciskiem na górze!")
        return

    # Pobranie danych z GUI
    data_wybrana = kalendarz.get_date()
    godzina = int(suwak_godzina.get())
    minuta = int(suwak_minuta.get())
    sekunda = int(suwak_sekunda.get())
    graniczna = datetime(data_wybrana.year, data_wybrana.month, data_wybrana.day, godzina, minuta, sekunda)

    # Odczyt pliku
    try:
        with open(sciezka_pliku, encoding='utf-8') as fin:
            linie = fin.readlines()
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Nie znaleziono pliku na dysku!")
        return
    except Exception as e:
        messagebox.showerror("Błąd", f"Problem z otwarciem pliku:\n{e}")
        return

    ostatnia_pasyjna_idx = -1
    ostatnia_pasyjna_linia = ""

    # --- UNIWERSALNE PARSOWANIE DATY ---
    # Formaty, które próbujemy dopasować
    formaty_dat = [
        '%Y-%m-%d %H:%M:%S',  # Np. 2025-12-06 09:38:08 (Twój obecny plik)
        '%Y/%m/%d %H:%M:%S',  # Np. 2025/12/06 09:38:08
        '%d.%m.%Y %H:%M:%S'   # Np. 06.12.2025 09:38:08
    ]

    for i, line in enumerate(linie):
        # Pobieramy pierwsze 19 znaków, aby odciąć milisekundy (np. ,062)
        if len(line) < 19:
            continue
            
        tekst_data = line[:19]
        data_log = None

        # Pętla próbująca dopasować format
        for fmt in formaty_dat:
            try:
                data_log = datetime.strptime(tekst_data, fmt)
                break # Udało się, przerywamy pętlę formatów
            except ValueError:
                continue # Nie pasuje, próbujemy kolejny format

        # Jeśli po sprawdzeniu wszystkich formatów data nadal jest None, pomijamy linię
        if data_log is None:
            continue

        # Porównanie daty
        if data_log <= graniczna:
            ostatnia_pasyjna_idx = i
            ostatnia_pasyjna_linia = line

    # Weryfikacja wyników
    if ostatnia_pasyjna_idx == -1:
        messagebox.showinfo("Brak zmian", "Nie znaleziono linii wcześniejszej lub równej wybranej dacie.\nPlik pozostaje bez zmian.")
        info_label.config(text="Brak dopasowania daty.")
        return

    linie_zachowane = linie[ostatnia_pasyjna_idx:]
    usuniete = ostatnia_pasyjna_idx
    zachowane = len(linie_zachowane)
    
    # Podgląd operacji
    podglad = ostatnia_pasyjna_linia.strip()
    if len(podglad) > 60:
        podglad = podglad[:60] + "..."

    okno_msg = (
        f"Plik: {os.path.basename(sciezka_pliku)}\n\n"
        f"Linii do usunięcia: {usuniete}\n"
        f"Linii do zachowania: {zachowane}\n\n"
        f"Nowy początek pliku (pierwsza zachowana linia):\n{podglad}\n\n"
        "Czy chcesz nadpisać plik?"
    )

    if messagebox.askyesno("Potwierdź nadpisanie", okno_msg):
        try:
            with open(sciezka_pliku, 'w', encoding='utf-8') as fout:
                fout.writelines(linie_zachowane)
            info_label.config(text=f"Sukces! Plik przycięty. Zachowano {zachowane} linii.")
            messagebox.showinfo("Gotowe", "Operacja zakończona pomyślnie.")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać pliku:\n{e}")
    else:
        info_label.config(text="Anulowano przez użytkownika.")

# --- Budowa interfejsu (GUI) ---
root = tk.Tk()
root.title("Inteligentny filtr logów")

frame = ttk.Frame(root)
frame.pack(padx=15, pady=15)

# Wybór pliku
btn_plik = ttk.Button(frame, text="Wybierz plik loga", command=wybierz_plik)
btn_plik.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

label_plik_info = ttk.Label(frame, text="Nie wybrano pliku", foreground="gray")
label_plik_info.grid(row=0, column=2, sticky="w", padx=5, pady=(0, 10))

# Data
ttk.Label(frame, text="Data graniczna:").grid(row=1, column=0, sticky="e")
kalendarz = DateEntry(frame, width=12, background='darkblue', foreground='white',
                      borderwidth=2, year=2025, date_pattern='y-mm-dd')
kalendarz.grid(row=1, column=1, sticky="w")

# Godzina
ttk.Label(frame, text="Godzina:").grid(row=2, column=0, sticky="e")
suwak_godzina = ttk.Scale(frame, from_=0, to=23, orient='horizontal', command=aktualizuj_godzine)
suwak_godzina.set(0)
suwak_godzina.grid(row=2, column=1, sticky="ew")
label_godzina = ttk.Label(frame, text="00")
label_godzina.grid(row=2, column=2, sticky="w")

# Minuta
ttk.Label(frame, text="Minuta:").grid(row=3, column=0, sticky="e")
suwak_minuta = ttk.Scale(frame, from_=0, to=59, orient='horizontal', command=aktualizuj_minuta)
suwak_minuta.set(0)
suwak_minuta.grid(row=3, column=1, sticky="ew")
label_minuta = ttk.Label(frame, text="00")
label_minuta.grid(row=3, column=2, sticky="w")

# Sekunda
ttk.Label(frame, text="Sekunda:").grid(row=4, column=0, sticky="e")
suwak_sekunda = ttk.Scale(frame, from_=0, to=59, orient='horizontal', command=aktualizuj_sekunda)
suwak_sekunda.set(0)
suwak_sekunda.grid(row=4, column=1, sticky="ew")
label_sekunda = ttk.Label(frame, text="00")
label_sekunda.grid(row=4, column=2, sticky="w")

# Info o granicy
granica_label = ttk.Label(frame, text="Wybrana granica: —", font=("Arial", 9, "bold"))
granica_label.grid(row=5, column=0, columnspan=3, pady=(15, 5))

# Przycisk
przycisk = ttk.Button(frame, text="Filtruj i nadpisz plik", command=filtruj_log)
przycisk.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")

# Status
info_label = ttk.Label(frame, text="Gotowy", foreground="blue")
info_label.grid(row=7, column=0, columnspan=3)

aktualizuj_granice()
root.mainloop()