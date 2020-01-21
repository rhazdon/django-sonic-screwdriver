class Shell(object):
    __HEADER = "\033[95m"
    __OK_BLUE = "\033[94m"
    __OK_GREEN = "\033[92m"
    __WARNING = "\033[93m"
    __FAIL = "\033[91m"
    __ENDC = "\033[0m"
    __BOLD = "\033[1m"
    __UNDERLINE = "\033[4m"

    def msg(self, msg):
        return print(self.__OK_BLUE, "Sonic: ", msg, self.__ENDC)

    def success(self, msg):
        return print(self.__OK_GREEN, "Sonic: ", msg, self.__ENDC)

    def warn(self, msg):
        return print(self.__WARNING, "Sonic: ", msg, self.__ENDC)

    def fail(self, msg):
        return print(self.__FAIL, "Sonic: ", msg, self.__ENDC)

    def debug(self, msg):
        return print(self.__WARNING, "Sonic: Debug: ", msg, self.__ENDC)


shell = Shell()
