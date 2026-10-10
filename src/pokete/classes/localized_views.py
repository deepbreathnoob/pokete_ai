"""Initialize dormant singleton views after locale and hotkeys are loaded."""


def refresh_localized_views():
    from .deck import deck
    from .detail import detail
    from .inv.inv import inv
    from .inv.buy import buy
    from .movemap import movemap
    from .timer import clock
    from .side_loops import loading_screen

    for view in (deck, detail, inv, buy, movemap, loading_screen):
        view.__init__()
    clock.__init__(clock.time)
