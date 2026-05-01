# System Monitorowania i Analizy Meteorologicznej (aplikacjaAT)

## Opis Projektu

Aplikacja służy do gromadzenia, archiwizacji oraz wizualizacji danych pogodowych w czasie rzeczywistym. System łączy się z zewnętrznym API (OpenWeatherMap), przechowuje dane w dokumentowej bazie NoSQL (MongoDB) i prezentuje je użytkownikowi w formie interaktywnych wykresów oraz tabel. Projekt został w pełni skonteneryzowany przy użyciu technologii Docker.

---

## Główne Funkcjonalności

* **Dynamiczne Pobieranie Danych:** Możliwość sprawdzenia pogody dla dowolnego miasta na świecie za pomocą metody HTTP POST.
* **Baza NoSQL (MongoDB):** Skalowalne przechowywanie danych w formacie BSON, co pozwala na elastyczne zarządzanie historią pomiarów.
* **Moduł Inżynierii Danych (Seeder):** Generator syntetycznych zestawów danych (100 pomiarów historycznych) do testów wydajnościowych i analitycznych.
* **Eksport do CSV:** Funkcja generowania i pobierania arkuszy danych w formacie `.csv` do zewnętrznej analizy (np. w Excelu).
* **Wizualizacja Chart.js:** Dynamiczny wykres liniowy prezentujący trendy temperatury dla wybranej lokalizacji.

---

## Stos Technologiczny

* **Backend:** Python 3.10, Flask
* **Baza Danych:** MongoDB 7.0
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js)
* **Konteneryzacja:** Docker, Docker Compose
* **API:** OpenWeatherMap API

---

## Instalacja i Uruchomienie

### 1. Klonowanie repozytorium i konfiguracja
Upewnij się, że posiadasz zainstalowany Docker Desktop i jest on uruchomiony.

Stwórz plik `.env` w głównym katalogu i uzupełnij go:

```env
WEATHER_API_KEY=twoj_klucz_api
MONGO_USER=admin
MONGO_PASS=secret_password
```

### 2. Uruchomienie kontenerów
W terminalu (np. PowerShell w VS Code) wykonaj komendę:

```bash
docker compose up --build -d
```

### 3. Dostęp do aplikacji
Aplikacja jest dostępna pod adresem: `http://localhost:5000`

---

## Struktura Projektu

* `app.py` – Główna logika serwera, obsługa tras (routes) i komunikacja z MongoDB.
* `templates/index.html` – Warstwa prezentacji, silnik Jinja2 oraz skrypty Chart.js.
* `Dockerfile` – Instrukcja budowy obrazu aplikacji Python.
* `docker-compose.yml` – Orkiestracja serwisów `weather_app` oraz `weather_db`.
* `requirements.txt` – Lista zależności Pythona (Flask, pymongo, requests, python-dotenv).

---

## Rozwiązywanie Problemów (FAQ)

* **Błąd 401 (Unauthorized):** Oznacza, że klucz API jest nieaktywny lub błędny. OpenWeatherMap aktywuje nowe klucze do 24h.
* **Błąd 404 (Not Found):** Jeśli trasy `/seed` lub `/download` nie działają, upewnij się, że przebudowałeś kontenery za pomocą flagi `--build`.
* **Podkreślenia w VS Code:** Czerwone błędy w `index.html` przy klamrach `{{ }}` to błędy lintera — silnik Jinja2 przetworzy je poprawnie po stronie serwera.
