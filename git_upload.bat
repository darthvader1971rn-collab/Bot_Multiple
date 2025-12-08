@echo off
echo --- NAPRAWA I WYSYLANIE NA GITHUB ---

:: Ustawienie zmiennych (Tu wpisz poprawny login!)
set GITHUB_USER=darthvader1971rn-collab
set REPO_NAME=Bot_Multiple

:: 1. Inicjalizacja (bezpieczna)
if not exist .git (
    git init
    git branch -M main
)

:: 2. Dodanie wszystkich plików
echo Dodaje pliki do poczekalni...
git add .

:: 3. Zapisanie zmian (Commit)
set /p commit_msg="Wpisz opis zmian (np. Finalna wersja): "
git commit -m "%commit_msg%"

:: 4. Naprawa adresu zdalnego (Usuwamy bledny, dodajemy poprawny)
git remote remove origin
git remote add origin https://github.com/darthvader1971rn-collab/Bot_Multiple.git

:: 5. Weryfikacja adresu
echo.
echo Wysylam do: https://github.com/darthvader1971rn-collab/Bot_Multiple.git
echo.

:: 6. Wyslanie (Push)
git push -u origin main

echo.
echo --- ZAKONCZONO ---
pause