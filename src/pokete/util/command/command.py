import sys

from pokete.i18n import _ as tr

from .parse import parse


class Flag:
    def __init__(self, aliases: list[str], desc: str):
        self.aliases = aliases
        self.desc = desc

    def is_flag(self, flag: str):
        return flag in self.aliases


class Command:
    def __init__(
        self,
        name: str,
        desc: str,
        fn,
        flags: list[Flag] | None = None,
        commands: list["Command"] | None = None,
        additional_info: str = "",
        usage="[command] [options]...",
    ):
        self.name = name
        self.desc = desc
        self.fn = fn
        self.flags = (flags if flags is not None else []) + [
            Flag(["-h", "--help"], "Shows help for a specific command")
        ]
        self.additional_info = additional_info
        self.commands = commands if commands is not None else []
        self.usage = usage

    @staticmethod
    def __line_setter(lines: list[tuple[str, str]], line_spaces: int):
        return "\n".join(
            f"\t{line[0]}{' ' * (line_spaces - len(line[0]))}{line[1]}"
            for line in lines
        )

    def __print_help(self, ex: str):
        option_lines = [(command.name, tr(command.desc)) for command in self.commands]
        flag_lines = [("|".join(flag.aliases), tr(flag.desc)) for flag in self.flags]
        line_spaces = max((len(i[0]) for i in option_lines + flag_lines), default=0) + 8
        print(f"{self.name} -- {tr(self.desc)}\n")
        print(tr("Usage:"))
        print(f"    {ex}{' ' + self.usage if self.usage else ''} <flags>")
        for title, lines in (("Options:", option_lines), ("Flags:", flag_lines)):
            if lines:
                print("\n" + tr(title))
                print(self.__line_setter(lines, line_spaces))
        if self.additional_info:
            print("\n" + tr(self.additional_info))
        print("\nCopyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2025")

    def run(self, ex: str, options: list[str], flags: dict[str, list[str]]):
        if options:
            for c in self.commands:
                if c.name == options[0]:
                    c.run(f"{ex} {options[0]}", options[1:], flags)
                    return
        all_flags = [i for f in self.flags for i in f.aliases]
        for flag in flags:
            if flag not in all_flags:
                print(
                    tr(":: Error: Unknown flag `{flag}`, try `{ex} --help`").format(
                        flag=flag, ex=ex
                    )
                )
                sys.exit(2)
        if "--help" in flags or "-h" in flags:
            self.__print_help(ex)
            sys.exit(0)
        else:
            self.fn(ex, options, flags)


class RootCommand(Command):
    def exec(self):
        args = sys.argv
        options, flags = parse(args)
        self.run(args[0], options, flags)
