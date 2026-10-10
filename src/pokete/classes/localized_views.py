"""Initialize dormant singleton views after locale and hotkeys are loaded."""


def refresh_localized_views():
    from .deck import deck
    from .detail import detail
    from .inv.buy import buy
    from .inv.inv import inv
    from .movemap import movemap
    from .multiplayer.interactions.movemap_deco import movemap_deco
    from .side_loops import loading_screen
    from .timer import clock

    for view in (deck, detail, inv, buy, movemap, loading_screen):
        view.__init__()
    clock.__init__(clock.time)
    movemap_deco.__init__()
