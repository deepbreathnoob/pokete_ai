from pokete.i18n import _ as tr


class InvItem:
    """Item for the inventory
    ARGS:
        name: The item's generic name (healing_potion)
        pretty_name: The item's pretty name (Healing potion)
        desc: The item's description
        price: The item's price in the shop
        _fn: The associated method name in FightItems"""

    def __init__(
        self,
        name: str,
        pretty_name: str,
        desc: str,
        price: int | None,
        _fn: str | None = None,
    ):
        self.name: str = name
        self._pretty_name = pretty_name
        self._desc = desc
        self.price = price
        self.func = _fn

    @property
    def pretty_name(self):
        return tr(self._pretty_name)

    @property
    def desc(self):
        return tr(self._desc)
