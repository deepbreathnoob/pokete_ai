# Code review spolszczenia — punkt kontrolny

Data: 2026-10-11. Gałąź: `feat/polish-localization`, PR #1.
Zakres: zmiany spolszczenia względem `master`, ich poprawki, inicjalizacja i
odświeżanie UI, układ przy minimalnym rozmiarze terminala, katalog gettext,
niezmienność identyfikatorów oraz istniejące testy zapisu i mechanik gry.

## Pętla przeglądu

| Runda | Stan | Ustalenia i wykonane poprawki |
| --- | --- | --- |
| 1 | ✅ zakończona, 5 problemów poprawionych | Klawisze specjalne wywoływały assertion podczas odświeżania widoków; skrócony szyld opieki tworzył przejście w kolizji budynku; zawijanie nie ograniczało długich słów i wielu linii; nazwy ataków nie mieściły się w menu nauki; audyt katalogu nie sprawdzał dokładnego kontekstu, klucza liczby mnogiej i parametrów wszystkich form. |
| 2 | ✅ zakończona, 1 problem poprawiony | Aktywne powiadomienie traciło elementy mapy podczas odświeżania, a późniejsze usunięcie powodowało `ValueError`. Powiadomienie jest teraz odłączane i ponownie dołączane; kolejka pozostaje zachowana. |
| 3 | ✅ zakończona, 1 problem poprawiony | Menu ataków w walce miało stałą szerokość 25. Szerokość zależy teraz od etykiet; panel opisu mieści się obok niego przy 70 kolumnach, jest wyrównany w pionie i sprzątany przy zamknięciu. |
| 4 | ✅ zakończona, bez nowych ustaleń | Ponowny przegląd poprawek, danych katalogu i cyklu życia widoków oraz komplet kontroli poniżej nie wykazały kolejnych problemów w sprawdzonym zakresie. |
| 5 | ✅ zakończona, 2 problemy poprawione | Ponowny review: pierwszy atak z efektem specjalnym otwierał pusty panel opisu; brakujące przypisania klawiszy w zapisie nie uruchamiały odzyskiwania, ponieważ kod porównywał pusty ciąg do `None`. Dodano inicjalizację panelu i poprawiono wykrywanie brakujących przypisań. |
| 6 | ✅ zakończona, 1 problem poprawiony | `shutil.get_terminal_size` traktował eksportowane `COLUMNS`/`LINES` jako ważniejsze od rozmiaru TTY. Wspólny odczyt dla ekranu ładowania i obsługi zmiany rozmiaru korzysta najpierw z rzeczywistych wymiarów terminala; fallback działa nadal bez TTY. |
| 7 | ✅ zakończona, bez nowych ustaleń | Ponowne sprawdzenie inicjalizacji i przełączania paneli, odzyskiwania skrótów, wykrywania rozmiaru, testów regresji i uruchamiania PL/EN nie wykazało kolejnych problemów w sprawdzonym zakresie. |

Usunięto także potrójne tłumaczenie tej samej tablicy dialogów. Nazwy własne,
ID w zapisie i protokole oraz mechaniki pozostają zgodne z dotychczasowymi testami.

## Weryfikacja

- **80 testów zaliczonych**, w tym 20 przypadków regresji dodanych podczas obu przeglądów. Testy obejmują
  klawisze specjalne i kliknięcia etykiet, wszystkie szyldy w danych gry,
  długie słowa i wieloliniowe komunikaty, wszystkie nazwy ataków w menu nauki,
  powtarzane odświeżanie z aktywnym powiadomieniem i kolejką oraz wszystkie
  ataki i opisy efektów w walce w EN/PL na mapie 70 × 19 (terminal 70 × 20).
- Drugi przegląd: 8 nowych przypadków najpierw odtworzyło błędy panelu
  opisu i odzyskiwania skrótów lub sprawdziło rzeczywiste wymiary terminala
  oraz fallback bez TTY; wersje EN i PL są objęte testami panelu.
- Audyt: 956 wymaganych komunikatów, brak brakujących lub niekompletnych
  tłumaczeń, brak fuzzy i zduplikowanych kluczy katalogu.
- `msgfmt --check`, kompilacja Pythona oraz Ruff E4/E7/E9/F/I dla zmienionych
  plików Pythona: zaliczone.
- Testy PTY: gra, ekwipunek, drużyna, Poketedex, zegar i menu działają bez
  wyjątku w PL 70 × 20, PL 80 × 24 i EN 80 × 24.
- Wheel zbudowany; pliki PO/POT/MO w paczce są identyczne ze źródłami.

Nie przeprowadzono pojedynku z działającym zewnętrznym serwerem.
Wynik ostatniej rundy dotyczy sprawdzonego zakresu, nie jest gwarancją braku
wszelkich możliwych błędów w całym projekcie.

## Wznowienie

Przegląd ukończony; brak otwartych ustaleń. Pobierz gałąź i wykonaj polecenia
z `LOCALIZATION_PROGRESS.md`. Nowy problem należy odtworzyć testem, poprawić,
ponownie przejrzeć zmianę i dopisać kolejną rundę do tej tabeli.
Nie scalać automatycznie PR z `master`.
