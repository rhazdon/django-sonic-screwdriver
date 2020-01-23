import re
from codecs import getwriter
from sys import stderr, stdout

ANSCI_ESCAPE = re.compile(r"\x1b[^m]*m")
STDERR_WRITER = getwriter("utf-8")(stderr.buffer)
STDOUT_WRITER = getwriter("utf-8")(stdout.buffer)


def ansi_clean(string):
    return ANSCI_ESCAPE.sub("", string)


def write_to_stream(stream, msg):
    try:
        if STDOUT_WRITER.isatty():
            stream.write(msg)
        else:
            stream.write(ansi_clean(msg))
        stream.flush()
    except Exception:
        pass


class Shell:
    __HEADER = "\033[95m"
    __OK_BLUE = "\033[94m"
    __OK_GREEN = "\033[92m"
    __WARNING = "\033[93m"
    __FAIL = "\033[91m"
    __ENDC = "\033[0m"
    __BOLD = "\033[1m"
    __UNDERLINE = "\033[4m"

    def msg(self, msg, append_new_line=True):
        self.__out(msg, self.__OK_BLUE, append_new_line)

    def success(self, msg, append_new_line=True):
        self.__out(msg, self.__OK_GREEN, append_new_line)

    def warn(self, msg, append_new_line=True):
        self.__out(msg, self.__WARNING, append_new_line)

    def fail(self, msg, append_new_line=True):
        self.__out(msg, self.__FAIL, append_new_line)

    def debug(self, msg, append_new_line=True):
        self.__out(msg, self.__WARNING, append_new_line)

    def __text(self, msg, color):
        return "{}Sonic: {}{}".format(color, msg, self.__ENDC)

    def __out(self, msg, color=None, append_new_line=False):
        if msg is not None:
            msg = self.__text(msg, color)
            if append_new_line:
                msg += "\n"
            write_to_stream(STDOUT_WRITER, msg)


shell = Shell()
