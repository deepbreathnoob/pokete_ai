"""Terminal dimensions for interactive play and redirected CLI output."""

import os
import shutil


def terminal_size():
    """Prefer live TTY dimensions over potentially stale shell variables."""
    try:
        size = os.get_terminal_size()
        if size.columns > 0 and size.lines > 0:
            return size
    except OSError:
        pass
    return shutil.get_terminal_size(fallback=(80, 24))
