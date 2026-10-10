# Pokete — Grey Edition

[English](README.md) · [Jak grać](docs/HowToPlay.pl.md) · [Polska encyklopedia](docs/wiki.pl.md) · [Stan spolszczenia](docs/LOCALIZATION_PROGRESS.md)

Pokete to gra terminalowa inspirowana klasycznymi grami o łapaniu i trenowaniu
stworzeń. Zwiedzaj świat, zbieraj Pokete, rozwijaj drużynę i pokonuj trenerów.
Zaczynasz z Pokete Steini.

![Gra Pokete](assets/ss/ss01.png)

## Instalacja tego spolszczenia

Potrzebujesz Pythona 3.12 lub nowszego. Tłumaczenie znajduje się na gałęzi
`feat/polish-localization` tego repozytorium; wydanie z PyPI może go jeszcze
nie zawierać.

```sh
git clone --branch feat/polish-localization https://github.com/deepbreathnoob/pokete_ai.git
cd pokete_ai
python -m pip install -e .
python -m pokete --language pl
```

Na Windows można użyć `py` zamiast `python`. Wymagane zależności, w tym
`scrap_engine`, są instalowane przez pip. Katalog tłumaczeń jest dołączony do
pakietu: gracz nie musi instalować gettext ani kompilować tłumaczenia.

## Język i uruchamianie

```sh
python -m pokete --language pl --help
python -m pokete --language pl --no_audio
python -m pokete --language en
```

Możesz wybrać „Język (po restarcie)” w menu, zapisać grę i uruchomić ją ponownie.
Pierwszeństwo mają: opcja `--language`, ustawienie w zapisie, zmienna
`POKETE_LANGUAGE`, a następnie język angielski. Parametr `--save_dir KATALOG`
pozwala wybrać katalog zapisów i dzienników. Opcje `--no_mods` i `--no_audio`
wyłączają odpowiednio mody i dźwięk; `--log` włącza dziennik.

Starsze zapisy pozostają zgodne. Tłumaczenie zmienia etykiety, a identyfikatory
przedmiotów, map, natur i NPC zachowują dotychczasowe wartości.

## Pierwsze kroki

Poruszaj się klawiszami W, A, S, D. Wejście w wysoką trawę może rozpocząć walkę.
W walce wybierz `1`, aby zaatakować, `3`, aby użyć przedmiotu, albo `4`, aby
zmienić Pokete. Osłab dzikiego Pokete i użyj Poketeball, aby go złapać.
Poza walką `1` otwiera drużynę, `3` mapę, `4` ekwipunek, `5` Poketedex,
`6` zegar, `h` pomoc, a `e` menu. Enter zatwierdza, Esc lub `q` zamyka widok.
Etykiety w grze pokazują aktualnie przypisane klawisze.

Centrum Pokete pozwala uleczyć stworzenia i zarządzać całą kolekcją. Sklepy
sprzedają kule i mikstury. Czerwone kule na mapie zawierają przedmioty — zbierzesz
je, wchodząc na nie. Każdy typ ma swoje mocne i słabe strony; pełne zestawienie
znajdziesz w polskiej encyklopedii.

## Gra wieloosobowa i mody

Wybierz tryb wieloosobowy, podaj adres serwera (domyślny port: 9988) i nazwę
gracza. Wbudowane dialogi oraz komunikaty klienta są tłumaczone lokalnie.
Nazwy innych graczy i teksty dostarczone przez zewnętrzne mody lub serwery
pozostają treścią autora, jeśli nie mają wpisu w katalogu tłumaczeń.
Wymiana w menu interakcji jest obecnie niewdrożona w tej wersji gry.

Mody umieszcza się w katalogu `mods` i włącza w menu. Przykład znajduje się w
[mods/example.py](mods/example.py).

## Pakowanie i rozwój

```sh
python -m pip install build pytest polib
python tools/localization_catalog.py
python -m pytest src/tests -q
python -m build --wheel
```

Po zmianie pliku PO skompiluj MO poleceniem podanym w
[opisie lokalizacji](docs/Localization.md). Własne pakowanie przez PyInstaller
musi uwzględniać `--add-data="src/pokete/locales:pokete/locales"`, a także
zasoby i bibliotekę audio odpowiednią dla systemu. Kod biblioteki audio i
instrukcje jej kompilacji są w [playsound](playsound/README.md).

Gra i spolszczenie są udostępniane na licencji GPLv3. Imiona, nazwy własne Pokete,
adresy projektu i informacje o autorach zachowano. Przykładowe zrzuty ekranu
pochodzą z angielskiej wersji. Dialogi zachowują humor i wulgaryzmy oryginału.
