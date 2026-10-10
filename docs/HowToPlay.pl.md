# Pokete — jak grać

[Uruchamianie](../README.pl.md) · [Encyklopedia](wiki.pl.md)

## Cel gry

Wyruszasz w świat jako młody trener. Łap Pokete, rozwijaj je i zdobywaj
osiągnięcia. Po drodze spotkasz mieszkańców, trenerów, zadania i areny.
Niektórzy rozmówcy są pomocni, inni prowokują lub używają wulgaryzmów.

## Sterowanie

Poniższa tabela opisuje domyślne przypisania. Własne przypisania są zapisywane
w grze, a etykiety i pomoc pokazują aktualne klawisze.

| Klawisz | Poza walką | W walce |
| --- | --- | --- |
| W/A/S/D | Ruch; nawigacja w menu | Nawigacja w menu |
| Enter / spacja | Zatwierdzenie | Zatwierdzenie |
| Esc / Q | Zamknięcie widoku | Zamknięcie podmenu |
| 1 | Drużyna | Ataki |
| 2 | Wyjście z gry | Próba ucieczki |
| 3 | Mapa świata | Przedmioty |
| 4 | Ekwipunek | Wybór Pokete |
| 5 | Poketedex | — |
| 6 | Zegar | — |
| H | Pomoc | — |
| E | Menu ustawień | — |
| R | Usunięcie przedmiotu w ekwipunku | — |

Postać gracza to małe `a`. Rozmowy przewijasz dowolnym klawiszem.
Możesz także używać myszy na obsługiwanych elementach menu.
Terminal powinien mieć co najmniej 70 kolumn i 20 wierszy.

## Walka i łapanie

Wysoka trawa, woda lub piasek mogą kryć dzikie Pokete. Wybierz atak i zatwierdź
Enterem albo klawiszem przypisanym do jego numeru. AP oznacza liczbę pozostałych
użyć danego ataku, HP — zdrowie, a XP — doświadczenie. Typ ataku i typ przeciwnika
wpływają na obrażenia; pogoda oraz efekty również mogą zmienić przebieg walki.

Aby złapać dzikiego Pokete, najpierw osłab go, następnie otwórz przedmioty
klawiszem `3` i użyj Poketeball, Superball lub Hyperball. Próba może się nie udać.
W pojedynku z trenerem nie można uciec ani złapać jego stworzenia. Za wygraną
otrzymasz $20. Gdy cała aktywna drużyna straci przytomność, wrócisz do ostatniego
centrum i stracisz część pieniędzy.

## Drużyna, rozwój i Poketedex

Aktywna drużyna liczy do sześciu Pokete. W centrum zobaczysz całą kolekcję,
zmienisz kolejność stworzeń i uleczysz je. Menu drużyny pozwala wypuszczać Pokete,
ale nie wszystkie naraz. Widok szczegółów pokazuje ataki, typ, naturę, statystyki
oraz zdolności. Pokete z atakiem „Lot” może przenieść cię do odwiedzonego miasta.

Pokete zdobywa XP i awansuje. Co piąty poziom może spróbować nauczyć się nowego
ataku. Maksymalnie zna cztery — wybierz, który zastąpić, lub anuluj naukę.
Płytki nauki uczą specjalnych ataków i zużywają się po użyciu. Przysmak zwiększa
poziom o jeden. Niektóre gatunki ewoluują po osiągnięciu odpowiedniego poziomu.

Poketedex (`5`) pokazuje gatunki złapane kiedykolwiek, ich opis, statystyki,
aktywność dzienną/nocną i ewolucję. Nieznane gatunki są oznaczone `???`.
Błyszczące Pokete są rzadkie (szansa 1/500); mają o 2 punkty więcej ataku,
obrony i inicjatywy oraz o 5 HP więcej. Ich nazwy są wyróżnione na żółto.

## Przedmioty i usługi

W ekwipunku (`4`) zobaczysz posiadane przedmioty i pieniądze. Enter pokazuje
opis lub rozpoczyna użycie przedmiotu, `R` usuwa wybrany przedmiot.
Mikstury leczą lub uzupełniają AP. Czerwone kule na mapie zawierają losowy łup.

Podejdź do osoby za ladą w centrum lub sklepie. Centrum leczy wszystkie Pokete,
pokazuje całą drużynę i pozwala przytulić wybranego Pokete. Sklep sprzedaje kule
i mikstury za pieniądze. Ośrodek opieki trenuje jednego pozostawionego Pokete;
wróć po niego później, aby odebrać je wraz ze zdobytym doświadczeniem.

Mapa świata (`3`) pokazuje miasta i drogi. Nawiguj klawiszami ruchu i sprawdzaj
opisy odwiedzonych miejsc. Legenda oznacza centrum jako `P`, sklep jako `$`,
opiekę jako `C`, a arenę jako `A`.

## Zapisy, język i multiplayer

Menu (`E`) pozwala zmienić nazwę gracza, znak postaci, animacje, dźwięk,
głośność, mody i automatyczny zapis. Zapisz grę przed wyjściem. Wybór języka
z menu wymaga zapisu i restartu. Możesz od razu uruchomić polski interfejs przez
`python -m pokete --language pl`.

Tryb wieloosobowy wybierasz przed wejściem do świata. Potrzebny jest działający
serwer zgodny z wersją klienta. Podaj adres i nazwę gracza. Menu interakcji
z innym graczem pozwala poprosić o pojedynek; opcja wymiany jest w tej wersji
jeszcze niewdrożona. Opisy dawnych mechanizmów wymiany w angielskiej instrukcji
mogą odnosić się do wcześniejszych wersji.
