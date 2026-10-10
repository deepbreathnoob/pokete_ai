"""Contains some small loops"""

import shutil

import scrap_engine as se

import pokete.base.game_map as gm
from pokete import release
from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.ui.views.boxes import InfoBoxView
from pokete.i18n import _
from pokete.util import liner


class LoopBox:
    """Provides an loops.easy_exit call function
    ARGS:
        box: The box to display"""

    def __init__(self, box):
        self.box = box

    def __call__(self, ctx: Context):
        """Shows the about text"""
        self.box.set_ctx(ctx)
        ctx = change_ctx(ctx, self.box)
        with self.box:
            loops.easy_exit(ctx)


class About(LoopBox):
    """The about text, that can be triggered in the menu"""

    def __init__(self):
        super().__init__(
            InfoBoxView(
                liner(
                    _(
                        "Pokete v{version} -- {codename}\nby lxgr-linux <lxgr@protonmail.com>\n\nThis software is licensed under GPLv3. A copy of the license is included with the game.\nContributions, especially new Poketes, are welcome:\nhttps://github.com/lxgr-linux/pokete"
                    ).format(version=release.VERSION, codename=release.CODENAME),
                    60,
                ),
                name=_("About"),
            )
        )


class Help(LoopBox):
    """Helptext that can be displayed by pressing '?'"""

    def __init__(self):
        super().__init__(
            InfoBoxView(
                liner(
                    _(
                        "Controls:\n{up}: up, {left}: left\n{down}: down, {right}: right\n{menu}: menu\n\nIn tall grass (;), wild Poketes may attack you.\nWeaken them to catch them, or defeat them to gain XP.\nApproach NPCs to talk to them.\nMore information:\nhttps://github.com/deepbreathnoob/pokete_ai/blob/master/docs/HowToPlay.md"
                    ).format(
                        up=Action.UP.mapping,
                        left=Action.LEFT.mapping,
                        down=Action.DOWN.mapping,
                        right=Action.RIGHT.mapping,
                        menu=Action.MENU.mapping,
                    ),
                    60,
                ),
                name=_("Help"),
            )
        )


class LoadingScreen:
    """Loading screen that's shown at game's start"""

    def __init__(self):
        width, height = shutil.get_terminal_size(fallback=(80, 24))
        self.map = gm.GameMap(width=width, height=height - 1)
        se.Text(
            r""" _____      _        _
|  __ \    | |      | |
| |__) |__ | | _____| |_ ___
|  ___/ _ \| |/ / _ \ __/ _ \
| |  | (_) |   <  __/ ||  __/
|_|   \___/|_|\_\___|\__\___|""",
            state="float",
        ).add(self.map, int(self.map.width / 2) - 15, int(self.map.height / 2) - 4)
        se.Text(f"v{release.VERSION}", state="float").add(
            self.map, int(self.map.width / 2) - 15, int(self.map.height / 2) + 2
        )
        se.Text(release.CODENAME, state="float").add(
            self.map,
            int(self.map.width / 2) + 14 - len(release.CODENAME),
            int(self.map.height / 2) + 2,
        )

    def __call__(self):
        """Shows the loading screen"""
        self.map.show()


loading_screen = LoadingScreen()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
