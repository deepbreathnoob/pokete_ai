"""This file contains all classes related to mods"""

import logging
import sys

import pokete.data as p_data
from pokete.base.ui.views.boxes import InfoBoxView
from pokete.i18n import _ as tr
from pokete.i18n import ngettext

from .settings import settings
from .side_loops import LoopBox


class DummyMods:
    """Dummy Mods class used when mods are disabled"""

    def __init__(self):
        self.mod_info = {}
        self.mod_obs = []
        self.mod_names = []


class ModError(Exception):
    """
    An Error that is thrown, when an inproper module is loaded
    ARGS:
        name: The mod's name
        err: The error that was thrown"""

    def __init__(self, name, err):
        self.name = name
        self.err = err
        super().__init__(
            tr("The mod '{name}' lacks attributes!\n{err}").format(name=name, err=err)
        )


class ModInfo(LoopBox):
    """Gives information about mods"""

    def __init__(self):
        count = len(loaded_mods.mod_info)
        state = (
            tr("Mods are enabled!")
            if settings("load_mods").val
            else tr("Mods are disabled!")
        )
        self.text = (
            state
            + "\n"
            + tr("To load a mod, place it in '/mods' and enable mods in the menu.")
        )
        self.text += "\n\n" + ngettext(
            "Currently {count} mod is loaded:",
            "Currently {count} mods are loaded:",
            count,
        ).format(count=count)
        self.text += (
            "\n   "
            + "\n   ".join(
                f"{name}-{info}" for name, info in loaded_mods.mod_info.items()
            )
            + "\n"
        )
        super().__init__(
            InfoBoxView(
                self.text,
                name=tr("Mods"),
            )
        )


def try_load_mods(_map):
    global loaded_mods
    if settings("load_mods").val:
        try:
            import mods
        except ModError as mod_err:
            error_box = InfoBoxView(str(mod_err), tr("Mod-loading Error"))
            error_box.center_add(_map)
            _map.show()
            sys.exit(1)

        for mod in mods.mod_obs:
            mod.mod_p_data(p_data)
    else:
        loaded_mods = DummyMods()
    logging.info(
        "[General] %d mods are loaded: (%s)",
        len(loaded_mods.mod_obs),
        ", ".join(loaded_mods.mod_names),
    )


loaded_mods = DummyMods()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
