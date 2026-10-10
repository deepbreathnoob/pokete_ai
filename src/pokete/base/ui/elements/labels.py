from scrap_engine import Area

from pokete.base.context import Context
from pokete.base.input import (
    Action,
)
from pokete.base.input.event import _ev
from pokete.base.input.key import Key
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements.text import HightlightableText
from pokete.i18n import _


def action_key_label(action: Action) -> str:
    """Readable label for the first currently assigned key."""
    names = {
        "Key.space": _("Space"),
        "Key.enter": _("Enter"),
        "Key.esc": _("Esc"),
        "Key.backspace": _("Backspace"),
        "Key.up": _("Up"),
        "Key.down": _("Down"),
        "Key.left": _("Left"),
        "Key.right": _("Right"),
    }
    return names.get(action.mapping, action.mapping)


class GenericActionLabel(HightlightableText, MouseInteractor):
    def __init__(self, action: Action, text: str):
        self.action = action
        assert action.mapping is not None and len(action.mapping) == 1, (
            "Trying to create Actionlabel with noch char mapping"
        )
        self.key = Key(action.mapping)
        super().__init__(f"{action.mapping}:{text}")

    def get_interaction_areas(self) -> list[Area]:
        return [self.get_area()]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx == 0:
            match event.type:
                case MouseEventType.MOVE:
                    self.highlight()
                case MouseEventType.LEFT:
                    if event.pressed:
                        _ev.set(self.key)
        else:
            self.un_highlight()


class CloseLabel(GenericActionLabel):
    def __init__(self):
        super().__init__(Action.CANCEL, _("close"))
