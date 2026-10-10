"""Contains class related to connecting to a server"""

from pokete import release
from pokete.base.context import Context
from pokete.base.input_loops import ask_ok, ask_text
from pokete.i18n import _ as tr
from pokete.util import liner

from .communication import ConnectionException, com_service
from .exceptions import (
    InvalidPokeException,
    UserPresentException,
    VersionMismatchException,
)
from .host_port import HostPort, HostPortParseException

DEFAULT_PORT = 9988


class Connector:
    """Manages server connection"""

    def __init__(self):
        self.host_port: HostPort = HostPort("localhost")
        self.user_name = ""
        self.saved_pos = ()

    def __call__(self, ctx: Context) -> bool:
        """Starts ui to connect to server"""
        conn_succ = False
        while not conn_succ:
            if not self.set_host_port(ctx):
                return False
            if not self.ask_user_name(ctx):
                continue
            conn_succ = self.establish_connection(ctx)
        self.handshake(ctx)
        return True

    def handshake(self, ctx: Context):
        try:
            greeting_text = com_service.handshake(ctx, self.user_name, release.VERSION)
            ask_ok(ctx, liner(greeting_text, ctx.map.width - 4))
        except UserPresentException:
            self.ask_user_name(ctx, True)
            self.establish_connection(ctx)
            self.handshake(ctx)
        except VersionMismatchException as e:
            ask_ok(ctx, tr("Version mismatch: {p0}").format(p0=e.version))
        except InvalidPokeException as e:
            ask_ok(ctx, tr("Invalid Poke: {p0}").format(p0=e.msg))

    def set_host_port(self, ctx: Context) -> bool:
        """Asks the user for host and port to connect to"""
        while True:
            host = ask_text(
                ctx,
                tr("Please enter the servers host you want to connect to."),
                tr("Host:"),
                str(self.host_port),
                tr("Host"),
                40,
            )
            if host is None:
                return False
            try:
                self.host_port = HostPort.parse(host)
            except HostPortParseException as e:
                ask_ok(ctx, tr("Error: {p0}").format(p0=e))
                continue
            break
        return True

    def ask_user_name(self, ctx: Context, reask=False) -> bool:
        """Asks the user for username
        ARGS:
            reask: Boolean whether or not this is asked again"""
        self.user_name = ctx.figure.name
        name = ask_text(
            ctx,
            (tr("That username isn't available right now\n") if reask else "")
            + tr("Please enter the username you want to use on the server"),
            tr("Username:"),
            self.user_name,
            tr("Username"),
            20,
        )
        if name is None:
            return False
        self.user_name = name
        return True

    def establish_connection(self, ctx):
        """Actually connects to the server"""
        try:
            com_service.connect(
                self.host_port.host,
                (
                    self.host_port.port
                    if self.host_port.port is not None
                    else DEFAULT_PORT
                ),
            )
        except ConnectionException as excpt:
            ask_ok(
                ctx,
                tr("An error occurred connecting to {p0} :\n{p1}").format(
                    p0=self.host_port, p1=excpt
                ),
            )
            return False
        return True


connector = Connector()
