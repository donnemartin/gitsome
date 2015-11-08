class GitSomeCommand(object):
    """Encapsulates members of a gitsome command.

    Attributes:
        * command: A string that represents the command.
        * expected_args: A list of expected arguments.
        * default_args: A list of default arguments.
        * method: A callable that executes the command.
    """

    def __init__(self, command, expected_args, default_args, method):
        """Initialized GitSomeCommand.

        Args:
            * command: A string that represents the command.
            * expected_args: A list of expected arguments.
            * default_args: A list of default arguments.
            * method: A callable that executes the command.

        Returns:
            None.
        """
        self.command = command
        self.expected_args = expected_args
        self.default_args = default_args
        self.method = method
