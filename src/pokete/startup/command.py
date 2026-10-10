import logging
import sys
from pathlib import Path

from pokete.i18n import _ as tr
from pokete.release import CODENAME, SAVEPATH, VERSION
from pokete.startup.language import configure_language
from pokete.util.command.command import Flag, RootCommand
from pokete.util.command.parse import parse


class PoketeCommand:
    language_flag = Flag(["--language"], "Interface language: en or pl")
    log_flag = Flag(["--log"], "Enables logging")
    mods_flag = Flag(["--no_mods"], "Disables mods")
    audio_flag = Flag(["--no_audio"], "Disables audio")
    save_dir_flag = Flag(
        ["--save_dir"],
        f"Sets the path for save-files and logs, default is: {SAVEPATH}",
    )

    def __init__(self, audio):
        self.language = None
        self.do_logging = False
        self.load_mods = True
        audio.use_audio = True
        self.audio = audio
        self.save_dir: Path = SAVEPATH

    def root_fn(self, ex: str, options: list[str], flags: dict[str, list[str]]):
        for flag, values in flags.items():
            if self.language_flag.is_flag(flag):
                if len(values) != 1 or values[0] not in ("en", "pl"):
                    print(
                        tr("--language expects exactly one argument: en or pl"),
                        file=sys.stderr,
                    )
                    sys.exit(2)
                self.language = values[0]
            elif self.log_flag.is_flag(flag):
                self.do_logging = True
            elif self.mods_flag.is_flag(flag):
                self.load_mods = False
            elif self.audio_flag.is_flag(flag):
                self.audio.use_audio = False
            elif self.save_dir_flag.is_flag(flag):
                if len(values) != 1:
                    logging.error(tr("Flag '%s' takes exactly one argument"), flag)
                    sys.exit(1)
                self.save_dir = Path(flags[flag][0])

    def run(self) -> tuple[bool, bool, Path]:
        _, parsed_flags = parse(sys.argv)
        self.root_fn(sys.argv[0], [], parsed_flags)
        configure_language(self.language, self.save_dir)
        self.save_dir_flag = Flag(
            ["--save_dir"],
            tr("Sets the path for save-files and logs, default is: {path}").format(
                path=SAVEPATH
            ),
        )
        c = RootCommand(
            "Pokete",
            f"{CODENAME} v{VERSION}",
            self.root_fn,
            flags=[
                self.language_flag,
                self.log_flag,
                self.mods_flag,
                self.audio_flag,
                self.save_dir_flag,
            ],
            additional_info=tr(
                "Save files and logs: {path}\nContributions are welcome. See README.md for details.\nThis software is licensed under GPLv3; a copy accompanies the game."
            ).format(path=SAVEPATH),
            usage="",
        )

        c.exec()

        return self.do_logging, self.load_mods, self.save_dir
