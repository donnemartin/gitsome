class GitSomeCommand(object):
    """Encapsulates members of a gitsome command.

    Attributes:
        * command: A string that represents the command.
        * expected_args_count: An int that represents the number of
            expected arguments.
        * expected_args_desc: A string of describing the expected arguments.
        * default_args: A list of default arguments.
        * method: A callable that executes the command.
    """

    def __init__(self, command, expected_args_count,
                 expected_args_desc, default_args, method):
        """Initialized GitSomeCommand.

        Args:
            * command: A string that represents the command.
            * expected_args_count: An int that represents the number of
                expected arguments.
            * expected_args_desc: A string of describing the expected arguments.
            * default_args: A list of default arguments.
            * method: A callable that executes the command.

        Returns:
            None.
        """
        self.command = command
        self.expected_args_count = expected_args_count
        self.expected_args_desc = expected_args_desc
        self.default_args = default_args
        self.method = method
