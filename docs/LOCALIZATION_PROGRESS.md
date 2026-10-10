# Spolszczenie — punkt wznowienia

Gałąź: `feat/polish-localization`. Nie scalać automatycznie z `master`.

## Fazy

| Faza | Stan | Zakres |
| --- | --- | --- |
| 1 | ✅ ukończona | gettext, `--language`, zapis ustawienia, podstawowe menu, pomoc |
| 2A | ✅ ukończona | nazwy wyświetlane niezależne od ID, inicjalizacja etykiet |
| 2B | 🔄 ostatni audyt | ekwipunek, drużyna, szczegóły, Pokédex, zegar, osiągnięcia |
| 3 | ✅ ukończona | walka, efekty, łapanie, rozwój i leczenie |
| 4 | ✅ ukończona | nazwy i opisy danych gry |
| 5 | ⬜ oczekuje | świat, dialogi, odpowiedzi, zadania i usługi |
| 6 | ⬜ oczekuje | multiplayer, CLI, instrukcja polska i audyt końcowy |

## Zasady

- Nigdy nie tłumaczyć kluczy zapisu, identyfikatorów map, NPC, ataków, typów,
  natur, przedmiotów ani wartości protokołu sieciowego.
- Nazwy własne Pokete oraz imiona pozostają nazwami własnymi.
- Pełne komunikaty tłumaczyć przed interpolacją parametrów.
- Angielski pozostaje obsługiwanym językiem i fallbackiem dla modów/serwerów.
- Po każdej fazie aktualizować tę tabelę, wyniki weryfikacji i następny krok.

## Weryfikacja i wznowienie

Faza 1: 38 testów zaliczonych; katalog sprawdzony `msgfmt`; wheel zawiera
katalogi; ręcznie sprawdzony wybór trybu w terminalu 80 × 24.

```sh
python -m pip install -e . pytest ruff build polib
python -m pytest src/tests
msgfmt --check -o src/pokete/locales/pl/LC_MESSAGES/pokete.mo src/pokete/locales/pl/LC_MESSAGES/pokete.po
python -m compileall -q src/pokete
```

Fazy 2A, 3 i 4: 43 testy zaliczone. Przetłumaczono 69 ataków, opisy
59 gatunków, 8 przedmiotów i dyski nauki, 4 pogody i 4 osiągnięcia.
Testy potwierdzają niezmienność ID/mechanik i parametrów szablonów.

**Następny krok:** zamknąć audyt fazy 2B (mody/natury), przetłumaczyć
dialogi i usługi (5), następnie CLI/multiplayer/instrukcję i audyt (6).
W razie przerwania najpierw sprawdzić `git status` i ten plik. Nie powtarzać faz
oznaczonych jako ukończone. Stan w toku nie oznacza zweryfikowanego ukończenia.
