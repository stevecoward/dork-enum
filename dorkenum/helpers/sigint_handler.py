import sys
from dorkenum import user_options


class SIGINT_handler():
    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, signal, frame):
        user_options['logger'].log(
            ('quitting so soon? and we were having so much fun...', 'white', 0))
        self.SIGINT = True
        sys.exit(0)
