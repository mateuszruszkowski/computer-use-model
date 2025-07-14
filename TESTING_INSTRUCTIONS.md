# Azure Computer Use Model - Instrukcje Testowania

## Wymagania wstępne

1. **Python 3.7 lub wyższy**
2. **System operacyjny:** Windows, macOS lub Linux
3. **Dostęp do Azure OpenAI** (wymaga aplikacji o dostęp: https://aka.ms/oai/cuaaccess)

## Konfiguracja środowiska - Windows

### 1. Klonowanie repozytorium
```powershell
git clone https://github.com/Azure-Samples/computer-use-model.git
cd computer-use-model\computer-use
```

### 2. Utworzenie środowiska wirtualnego Python
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Instalacja zależności
```powershell
pip install -r requirements.txt
```

Po ustawieniu zmiennych systemowych należy zrestartować PowerShell.

## Testowanie aplikacji

### Test podstawowy
```powershell
python main.py --instructions "Otwórz przeglądarkę i przejdź do microsoft.com"
```

### Dostępne parametry
- `--instructions`: Zadanie do wykonania (domyślnie: "Open web browser and go to microsoft.com")
- `--model`: Model AI do użycia (domyślnie: "computer-use-preview")
- `--endpoint`: Endpoint API ("azure" lub "openai", domyślnie: "azure")
- `--autoplay`: Automatyczne wykonywanie akcji bez potwierdzenia (domyślnie: true)

### Przykłady użycia

1. **Otworzenie kalkulatora:**
```powershell
python main.py --instructions "Otwórz kalkulator Windows"
```

2. **Napisanie dokumentu:**
```powershell
python main.py --instructions "Otwórz Notatnik i napisz 'Hello World'"
```

3. **Interakcja z przeglądarką:**
```powershell
python main.py --instructions "Otwórz przeglądarkę, wyszukaj 'Azure AI' w Google"
```

4. **Tryb interaktywny (wymagane potwierdzenie):**
```powershell
python main.py --autoplay false
```

5. **Bez sprawdzania bezpieczeństwa + monitorowanie tokenów:**
```powershell
python main.py --no-safety --log-tokens --instructions "Znajdź pogodę w Warszawie"
```

### Nowe opcje

- **`--no-safety`**: Wyłącza wszystkie sprawdzania bezpieczeństwa i automatycznie akceptuje akcje
- **`--log-tokens`**: Wyświetla statystyki użycia tokenów (przydatne do monitorowania kosztów)
- **`--resolution`**: Ustawia rozdzielczość dla modelu AI (domyślnie: 1024x768)
- **`--debug`**: Włącza szczegółowe logowanie debugowania

### Rozdzielczość ekranu

Model AI pracuje na przeskalowanych zrzutach ekranu. Możesz dostosować rozdzielczość:

```powershell
# Wyższa rozdzielczość dla lepszej dokładności
python main.py --resolution 1344x576 --no-safety --log-tokens --instructions "Używam windows 11, Otwórz Paint i narysuj koło"

# Standardowa rozdzielczość (domyślna)
python main.py --resolution 1344x576 --no-safety --log-tokens  --instructions "Używam windows 11, uzyj win+r i  Otwórz kalkulator, zmaksymalizuj okno i podaj wynik dzialania 5*5"

# Niższa rozdzielczość dla szybszego przetwarzania
python main.py --resolution 1344x576 --no-safety --log-tokens  --instructions "Używam windows 11, uzyj win+r i otwórz notatnik. Następnie napisz 'Witam Serdecznie, dziękuję za uwagę'"

python main.py --resolution 1344x576 --no-safety --log-tokens --instructions "Używam windows 11, uzyj win+r i otwórz przeglądarkę Edge. Następnie znajdź pogodę na dzisiaj w Warszawie"
```

### Rekomendowane rozdzielczości dla różnych ekranów

**Dla monitora ultrawide 3440x1440 (21:9):**
```powershell
# Najlepsza dokładność (zachowane proporcje 21:9)
python main.py --resolution 1680x720 --no-safety --instructions "Twoje zadanie"

# Dobry kompromis między dokładnością a szybkością
python main.py --resolution 1344x576 --no-safety --instructions "Twoje zadanie"

# Szybkie przetwarzanie
python main.py --resolution 1050x450 --no-safety --instructions "Twoje zadanie"
```

**Dla standardowych monitorów:**
- 16:9 (1920x1080, 2560x1440): użyj `1280x720` lub `1920x1080`
- 16:10 (1920x1200, 2560x1600): użyj `1280x800` lub `1680x1050`
- 4:3 (1024x768, 1280x1024): użyj `1024x768`

**Uwaga**: 
- Wyższa rozdzielczość = lepsza dokładność ale wolniejsze przetwarzanie i więcej tokenów
- Zachowanie proporcji ekranu jest ważne dla dokładności kliknięć
- Model ma limit 2048px na najdłuższym boku

## Jak działa aplikacja

1. **Przechwytywanie ekranu**: Model robi zrzuty ekranu aby "widzieć" interfejs
2. **Analiza wizualna**: AI analizuje obraz i określa jakie akcje wykonać
3. **Wykonanie akcji**: Symuluje kliknięcia myszy i naciśnięcia klawiszy
4. **Mechanizmy bezpieczeństwa**: Prosi o zgodę na potencjalnie niebezpieczne operacje

## Rozwiązywanie problemów

### Problem: "Module not found"
```powershell
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Problem: "Permission denied" przy kontrolowaniu myszy/klawiatury
- Uruchom PowerShell jako Administrator
- Dodaj wyjątek w programie antywirusowym dla Pythona

### Problem: "API key invalid"
- Upewnij się, że masz dostęp do Computer Use model (aplikuj: https://aka.ms/oai/cuaaccess)
- Sprawdź poprawność zmiennych środowiskowych:
```powershell
echo $env:AZURE_OPENAI_ENDPOINT
echo $env:AZURE_OPENAI_API_KEY
```

## Uwagi bezpieczeństwa

⚠️ **WAŻNE**: Model może kontrolować mysz i klawiaturę!
- Nie pozostawiaj modelu bez nadzoru
- Używaj trybu `--autoplay false` dla większej kontroli
- Model może prosić o zgodę przed wykonaniem potencjalnie niebezpiecznych akcji

## Ograniczenia

- Model działa najlepiej przy rozdzielczości skalowanej do 1024x768
- Niektóre aplikacje mogą być trudne do kontrolowania (np. gry)
- Model może nie rozpoznać wszystkich elementów interfejsu

## Dodatkowe zasoby

- [Dokumentacja Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)