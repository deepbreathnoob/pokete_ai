# Spolszczenie — punkt wznowienia

Gałąź: `feat/polish-localization`. Nie scalać automatycznie z `master`.

## Fazy

| Faza | Stan | Zakres |
| --- | --- | --- |
| 1 | ✅ ukończona | gettext, `--language`, zapis ustawienia, podstawowe menu, pomoc |
| 2A | ✅ ukończona | nazwy wyświetlane niezależne od ID, inicjalizacja etykiet |
| 2B | ✅ ukończona | ekwipunek, drużyna, szczegóły, Pokédex, zegar, osiągnięcia |
| 3 | ✅ ukończona | walka, efekty, łapanie, rozwój i leczenie |
| 4 | ✅ ukończona | nazwy i opisy danych gry |
| 5 | ✅ ukończona | świat, dialogi, odpowiedzi, zadania i usługi |
| 6 | ✅ ukończona | multiplayer, CLI, instrukcja polska i audyt końcowy |

## Zasady

- Nigdy nie tłumaczyć kluczy zapisu, identyfikatorów map, NPC, ataków, typów,
  natur, przedmiotów ani wartości protokołu sieciowego.
- Nazwy własne Pokete oraz imiona pozostają nazwami własnymi.
- Pełne komunikaty tłumaczyć przed interpolacją parametrów.
- Angielski pozostaje obsługiwanym językiem i fallbackiem dla modów/serwerów.
- Po każdej fazie aktualizować tę tabelę, wyniki weryfikacji i następny krok.

## Weryfikacja i wznowienie

**Wszystkie fazy ukończone.** Stan końcowy: 60 testów zaliczonych; 980
przetłumaczonych wpisów katalogu, w tym wszystkie 956 komunikatów wymaganych
przez audyt. Brak wpisów fuzzy i brak brakujących tłumaczeń w danych gry oraz
zasobach dołączonego serwera. Liczby obejmują także etykiety/nazwy własne,
które pozostają takie same w obu językach.

- `msgfmt --check`, kompilacja Pythona i lint zmienionych plików: zaliczone.
- Wheel: PO, POT i MO są dołączone i identyczne z plikami źródłowymi.
- Test PTY: polski wybór trybu i wprowadzenie; gra, ekwipunek, drużyna,
  Poketedex, zegar i menu bez wyjątków w PL 70 × 20, PL 80 × 24 oraz EN 80 × 24.
- Testy regresji: zgodność ID i mechanik, stare zapisy, klawisze, parametry
  komunikatów, polskie liczby mnogie, etykiety odpowiedzi oraz geometria szyldów.
- Test rozwoju: ewolucja wyświetla właściwą nazwę Pokete i zastępuje właściwy
  element drużyny. Naprawiono odkryte błędne odwołania do mapy zamiast Pokete.
- Multiplayer: sprawdzone katalogi, zasoby, teksty klienta i wybór odpowiedzi;
  nie przeprowadzono pojedynku z działającym zewnętrznym serwerem.

## Polecenia kontrolne

```sh
python -m pip install -e . pytest ruff build polib
python tools/localization_catalog.py
msgfmt --check -o src/pokete/locales/pl/LC_MESSAGES/pokete.mo src/pokete/locales/pl/LC_MESSAGES/pokete.po
python tools/build_polish_wiki.py
python -m pytest src/tests -q
python -m compileall -q src/pokete
python -m build --wheel
```

## Jak wznowić

1. Pobierz gałąź `feat/polish-localization`; sprawdź `git status` i `git log -1`.
2. Przeczytaj ten plik oraz `docs/Localization.md`.
3. Wykonaj polecenia kontrolne. Nie powtarzaj ukończonych faz.
4. Przy dodawaniu nowych tekstów rozszerz katalog i audyt, skompiluj MO,
   odtwórz polską encyklopedię, zaktualizuj ten punkt kontrolny i zapisz commit.

**Następny krok:** przegląd zmian i opcjonalny test pojedynku z serwerem.
Nie ma otwartej fazy tłumaczenia. Angielska dokumentacja techniczna,
licencja, changelogi, komentarze, diagnostyka techniczna i dowolne treści
zewnętrznych modów/serwerów nie należą do katalogu tłumaczeń interfejsu gry.
Nazwy własne i identyfikatory nie wymagają spolszczenia.
