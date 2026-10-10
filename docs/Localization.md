# Lokalizacja EN/PL — etap 1

Wybierz polski interfejs przy uruchomieniu:

```sh
python -m pokete --language pl
```

Możesz też wybrać `Język (po restarcie)` w menu gry, zapisać grę
lub zakończyć ją przez menu i uruchomić ponownie. Uruchomienie z
`--language en` przywraca angielski interfejs. Wybór z CLI jest zapisywany
w ustawieniach przy następnym zapisie gry.

Kolejność wyboru: `--language`, język zapisany w grze,
zmienna środowiskowa `POKETE_LANGUAGE`, domyślnie `en`.
Starsze zapisy bez ustawienia języka są nadal obsługiwane.

## Zakres

Etap 1 obejmuje menu ustawień, wybór trybu gry, pomoc podczas gry,
informacje o grze, wprowadzenie, etykiety zamykania i potwierdzeń oraz
ostrzeżenie o otwarciu zapisu w starszej wersji gry. Potwierdzenia i pomoc
wyświetlają aktualne przypisania klawiszy.

Opisy stworzeń, ataków i przedmiotów, dialogi NPC, komunikaty walki,
podmenu osiągnięć i modów, pomoc CLI i zasoby multiplayer pozostają
zadaniami kolejnych etapów. Sama zmiana języka nie przebudowuje istniejących
widoków, dlatego obowiązuje po restarcie gry.

## Rozwijanie tłumaczeń

- `src/pokete/i18n.py`: gettext, wybór języka i angielski tekst zastępczy.
- `src/pokete/locales/pokete.pot`: szablon komunikatów.
- `src/pokete/locales/pl/LC_MESSAGES/pokete.po`: polskie tłumaczenia.
- `src/pokete/locales/pl/LC_MESSAGES/pokete.mo`: skompilowany katalog,
  dołączany do paczki instalacyjnej; użytkownik nie potrzebuje `msgfmt`.

Tłumacz całe zdania przez `_()` i dopiero potem podstawiaj nazwane parametry:

```python
_("Received {amount} coins.").format(amount=amount)
```

Dla liczby mnogiej używaj `ngettext(singular, plural, count)`.
Polski katalog definiuje trzy formy liczby mnogiej. Nie dopisuj `s`
do nazwy przedmiotu i nie składaj zdania z tłumaczonych fragmentów.

Nie tłumacz identyfikatorów zapisów, nazw akcji, kluczy zasobów ani
nazw używanych przez rejestr NPC. Nazwy widoczne dla gracza powinny
być osobnymi etykietami. Nie edytuj ręcznie wygenerowanych klas zasobów.

Po zmianie tłumaczeń skompiluj katalog (pakiet `gettext`):

```sh
msgfmt --check -o src/pokete/locales/pl/LC_MESSAGES/pokete.mo \
    src/pokete/locales/pl/LC_MESSAGES/pokete.po
python -m pytest src/tests -q
```

Nowe komunikaty dopisuj też do pliku POT. Przed zatwierdzeniem sprawdź
polskie znaki, długości etykiet, parametry szablonów i zgodność ze starym zapisem.
