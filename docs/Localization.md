# Lokalizacja EN/PL

Uruchom polski interfejs przez `python -m pokete --language pl` albo wybierz
„Język (po restarcie)” w menu, zapisz grę i uruchom ponownie.
`--language en` przywraca angielski. Wybór z CLI jest zapisywany w ustawieniach
przy następnym zapisie gry.

Kolejność wyboru: `--language`, język zapisany w grze, `POKETE_LANGUAGE`, `en`.
Dotyczy także pomocy CLI. Starsze zapisy bez języka nadal działają.

## Zakres

Spolszczenie obejmuje interfejs gry, walkę, rozwój, katalog gatunków/ataków/
przedmiotów, mapy i ich opisy, dialogi i odpowiedzi NPC, zadania, usługi,
osiągnięcia, mody, klienta multiplayer, pomoc CLI i metadane aplikacji.
Polska instrukcja jest w `README.pl.md` i `docs/HowToPlay.pl.md`, a encyklopedia
w `docs/wiki.pl.md`. Postęp i instrukcje wznowienia: `LOCALIZATION_PROGRESS.md`.

Nazwy własne gatunków, imiona, nazwy użytkowników, identyfikatory zapisów i
protokołu pozostają oryginalne. Angielska dokumentacja techniczna, licencja,
historyczne changelogi, komentarze i diagnostyka techniczna pozostają źródłem
angielskim. Dowolne teksty napisane przez autorów zewnętrznych modów/serwerów
wymagają osobnych wpisów w katalogu; nie są automatycznie tłumaczone.
Klient tłumaczy sprawdzone teksty zasobów dołączonego serwera.

Wybór języka w menu działa po restarcie. Widoki singletonów są przebudowywane
przy starcie i po odczycie przypisań klawiszy. Przedmioty udostępniają nazwy
wyświetlane oddzielnie od ID; zasoby bazowe są kopiowane do warstwy wyświetlania.
Dialogi i odpowiedzi są tłumaczone przed obliczeniem wymiarów oraz animacją.
Wybór odpowiedzi nadal zwraca pierwotny klucz, wymagany przez logikę dialogu.

## Rozwijanie tłumaczeń

- `src/pokete/i18n.py`: gettext, wybór języka, fallback i adaptery wyświetlania.
- `src/pokete/locales/pokete.pot`: kompletny szablon komunikatów.
- `src/pokete/locales/pl/LC_MESSAGES/pokete.po`: polskie tłumaczenia.
- `src/pokete/locales/pl/LC_MESSAGES/pokete.mo`: skompilowany katalog w pakiecie.
- `tools/localization_catalog.py`: odtworzenie POT i kontrola pokrycia danych.
- `tools/build_polish_wiki.py`: odtworzenie polskiej encyklopedii.

Tłumacz komunikat przed interpolacją, np.:

```python
from pokete.i18n import _ as tr
tr("Received {amount} coins.").format(amount=amount)
```

Alias `tr` zapobiega konfliktom ze zmienną `_` używaną w pętlach gry.
Używaj nazwanych parametrów. Część istniejących komunikatów używa pozycyjnie
nazwanych parametrów `p0`, `p1` — ich zestaw musi pozostać niezmieniony.
Dla liczby mnogiej stosuj `ngettext`; polski katalog ma trzy formy.
Lista przedmiotów używa zapisu „nazwa × liczba”, bez angielskiego przyrostka `s`.
`pgettext("nature", name)` odróżnia nazwę natury od nazwy typu.

Nie tłumacz identyfikatorów, kluczy zasobów i nazw akcji protokołu. Nie edytuj
ręcznie wygenerowanych klas zasobów. Napisy na budynkach muszą zachować
wymiary i położenie pustych znaków, bo wpływają na kolizje.

```sh
python -m pip install -e . pytest polib build
python tools/localization_catalog.py
msgfmt --check -o src/pokete/locales/pl/LC_MESSAGES/pokete.mo \
    src/pokete/locales/pl/LC_MESSAGES/pokete.po
python tools/build_polish_wiki.py
python -m pytest src/tests -q
python -m build --wheel
```

`polib` i `msgfmt` są potrzebne podczas rozwoju tłumaczenia, nie do gry.
Audyt obejmuje wszystkie wpisy `tr`/`_`, wskazane dynamiczne etykiety oraz
teksty danych gry; nowe ścieżki wyświetlania należy dopisać do audytu.
Sprawdź też ręcznie długości polskich etykiet i działanie w terminalu 70 × 20.
