"""All classes needed for Item management"""

from pokete.classes.asset_service.resources.base.attacks import Attack
from pokete.i18n import _ as tr

from .invitem import InvItem


class LearnDisc(InvItem):
    """Learning disc item to teach attacks to Poketes
    ARGS:
        attack_name: The name of the attack being taught"""

    def __init__(self, attack_name: str, attack: Attack):
        self.attack_name = attack_name
        self.attack: Attack = attack
        pretty_name = f"LD-{self.attack.name}"
        name = f"ld_{attack_name}"
        desc = f"Teaches a Pokete the attack '{self.attack.name}'."
        super().__init__(name, pretty_name, desc, 0)

    @property
    def pretty_name(self):
        return tr("LD-{attack}").format(attack=tr(self.attack.name))

    @property
    def desc(self):
        return tr("Teaches a Pokete the attack '{attack}'.").format(
            attack=tr(self.attack.name)
        )
