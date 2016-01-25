import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class IdmToolsApp(App):

    def __init__(self):
        super(IdmToolsApp, self).__init__(
            description='Some tools to help with common tasks using FIWARE IdM Keyrock',
            version='5.1',
            command_manager=CommandManager('idmadmin.tools'),
            deferred_help=True,
        )


def main(argv=sys.argv[1:]):
    myapp = IdmToolsApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))