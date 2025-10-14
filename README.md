# Projekt wykonany w ramach kursu IT STEP ACADEMY

# 🏠 Smart Home System – Aplikacja Webowa Django z MQTT

## 📌 Opis projektu

**Smart Home System** to aplikacja webowa służąca do zarządzania inteligentnym domem, oparta na frameworku **Django** oraz protokole **MQTT**. Umożliwia zdalne sterowanie urządzeniami IoT (takimi jak światła, gniazdka, czujniki temperatury i ruchu), wizualizację danych pomiarowych oraz tworzenie automatycznych scenariuszy (reguł).

Projekt integruje się z urządzeniami typu **ESP32/ESP8266** lub dowolnym innym klientem MQTT, obsługuje wielu użytkowników, gromadzi historię zdarzeń oraz pozwala na dynamiczną rozbudowę o nowe moduły.

---

## 🌟 Kluczowe funkcjonalności

### 1. 🔐 System użytkowników
- Rejestracja i logowanie użytkowników.
- Panel użytkownika z przeglądem urządzeń, danych i aktywności.
- Obsługa sesji, zabezpieczeń i ról użytkowników (np. administrator).

### 2. 💡 Zdalne sterowanie urządzeniami (MQTT)
- Włączanie/wyłączanie urządzeń w czasie rzeczywistym za pomocą tematów MQTT.
- Obsługa czujników (odczyt danych) i aktuatorów (wydawanie poleceń).
- Powiązanie tematów MQTT z urządzeniami przypisanymi do użytkowników.

### 3. 🧠 Automatyzacja i reguły
- Tworzenie reguł automatycznych, np. „włącz światło o 20:00” lub „gdy temperatura < 18°C, uruchom grzejnik”.
- Harmonogramy oraz warunki logiczne.
- Przechowywanie i edycja reguł przez GUI.

### 4. 📋 Lista i zarządzanie urządzeniami
- Dodawanie, edytowanie i usuwanie urządzeń.
- Przypisywanie nazw, ikon, pokoi oraz tematów MQTT.
- Podgląd statusu (online/offline) oraz ostatniej aktywności.

### 5. 📈 Wizualizacja danych
- Wykresy danych historycznych z czujników (temperatura, wilgotność, ruch itd.).
- Integracja z bibliotekami **Plotly** lub **Matplotlib**.
- Możliwość filtrowania danych według daty, urządzenia, zakresu czasu.

### 6. 📜 Historia zdarzeń
- Rejestrowanie wszystkich interakcji użytkownika i urządzeń.
- Logi dostępne z panelu użytkownika (kto, kiedy, co zrobił).
- Eksport historii do pliku CSV.

### 7. ⚙️ Panel administracyjny i ustawienia
- Konfiguracja globalnych ustawień aplikacji:
  - Adres i port brokera MQTT.
  - Domyślne reguły automatyzacji.
  - Personalizacja nazw urządzeń.
- Zarządzanie kontami użytkowników i urządzeniami.

---

## 🗺️ Roadmapa i struktura aplikacji 

Aplikacja będzie składać się z czterech głównych ekranów widocznych po zalogowaniu się użytkownika. Każdy z nich realizuje konkretne funkcje związane z zarządzaniem inteligentnym domem.

### 🖥️ 1. Dashboard (Strona główna)
Cel: Centralny punkt zarządzania – szybki podgląd stanu systemu, aktywności i skróty do najważniejszych funkcji.

Zawartość:

🔸 Widżety z aktualnymi danymi z czujników (np. temperatura, ruch, światło, wilgotność).

🔸 Skróty do najczęściej używanych urządzeń (np. światło w salonie – przycisk WŁ/WYŁ).

🔸 Ostatnie zdarzenia (np. „Światło w kuchni wyłączone przez użytkownika Anna, 12:43”).

🔸 Powiadomienia systemowe (np. „Temperatura poniżej progu: 17°C”).

## 💡 2. Urządzenia (Devices)
Cel: Zarządzanie wszystkimi urządzeniami IoT przypisanymi do danego użytkownika.

Zawartość:

🔸 Lista urządzeń w formie tabeli lub kafelków (nazwa, typ, status, pokój, ostatnia aktywność).

🔸 Możliwość dodania nowego urządzenia z formularzem:

Nazwa, opis

Typ (czujnik / aktuator)

Pokój (salon, kuchnia…)

Temat MQTT (np. home/livingroom/light1)

🔸 Edycja i usuwanie istniejących urządzeń.

🔸 Ikony / kolory reprezentujące status (zielony: online, szary: offline).

## 📈 3. Historia i statystyki
Cel: Analiza i archiwizacja danych z urządzeń – zarówno logi zdarzeń, jak i pomiary z czujników.

Zawartość:

🔸 Filtrowalne logi użytkowników i urządzeń:

Co, kiedy, przez kogo

Eksport do CSV

🔸 Interaktywne wykresy danych pomiarowych:

Temperatura, wilgotność, ruch

Wybór przedziału czasu, urządzenia

🔸 Wskaźniki dzienne/tygodniowe/miesięczne aktywności.

## ⚙️ 4. Automatyzacja i ustawienia
Cel: Konfiguracja działania systemu – reguły automatyzacji, MQTT oraz ustawienia konta.

Zawartość:

🧠 Reguły automatyzacji
🔧 Ustawienia systemu
👤 Ustawienia konta:

---

## 🛠️ Technologie

- **Backend:** Python 3.10, Django 4.x
- **MQTT:** `paho-mqtt`, broker Mosquitto lub ESP32 jako klient
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Baza danych:** SQLite (domyślnie), PostgreSQL (opcjonalnie)
- **Wizualizacja danych:** Matplotlib, Plotly
- **Protokół komunikacji:** MQTT

---

## 🚀 Jak uruchomić projekt (dla początkujących z Django)

### 🔧 Czym jest Django?

**Django** to wysokopoziomowy framework webowy dla Pythona, który umożliwia szybkie tworzenie aplikacji internetowych w architekturze MVC (Model-View-Controller). Django automatycznie generuje panele administracyjne, obsługuje formularze, routing, bazę danych, logowanie, i wiele więcej.

---

## ▶️ Szybki start – krok po kroku

### 1. 📦 Klonowanie repozytorium

```bash
git clone https://github.com/twoje_repo/smart-home-system.git
cd smart-home-system
```

### 2. 🐍 Tworzenie i aktywacja środowiska wirtualnego
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. 📦 Instalacja zależności
```bash
pip install -r requirements.txt
```

### 4. 🛠️ Wykonanie migracji bazy danych
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 👤 Utworzenie konta administratora
```bash
python manage.py createsuperuser
```

### 6. 🚀 Uruchomienie serwera developerskiego
```bash
python manage.py runserver
```
Aplikacja będzie dostępna pod adresem:
http://127.0.0.1:8000

---

## 📚 Dodatkowe informacje

Panel administratora: http://127.0.0.1:8000/admin
Domyślna lokalizacja konfiguracji MQTT: settings.py lub panel ustawień
Dokumentacja Django: https://docs.djangoproject.com/pl/

---

## ✅ Pomysły na rozszerzenia
- Powiadomienia push (np. WebSocket + Firebase)
- Aplikacja mobilna (React Native / Flutter)
- Integracja z Google Assistant / Alexa
- Obsługa Zigbee/Z-Wave
- System alarmowy i kamery
