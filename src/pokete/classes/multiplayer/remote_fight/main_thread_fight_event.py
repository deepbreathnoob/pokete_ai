import pokete.bs_rpc as bs_rpc
from pokete.base.context import Context
from pokete.base.input_loops.ask import ask_bool
from pokete.base.single_event import SingleEvent
from pokete.classes.multiplayer.remote_fight import remote_fight_controller
from pokete.i18n import _ as tr


class MainThreatFightEvent(SingleEvent):
    def __init__(self, name: str):
        self.__name: str = name
        self.__chan: bs_rpc.Channel[bool] = bs_rpc.Channel[bool]()

    def wait_accepted(self) -> bool:
        return not not self.__chan.listen()

    def run(self, ctx: Context):
        accept = ask_bool(
            ctx, tr("'{p0}' wants to start a fight with you").format(p0=self.__name)
        )
        self.__chan.push(accept)
        self.__chan.close
        remote_fight_controller.start(ctx, self.__name)
