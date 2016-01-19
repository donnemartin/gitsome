def format_repo(repo):
    """Formats a repo tuple for pretty print.

    Example:
        Input:  ('donnemartin', 'gitsome')
        Output: donnemartin/gitsome

    Args:
        * arg: A tuple that contains the user and repo.

    Returns:
        A string of the form user/repo.
    """
    return '/'.join(repo)

def listify(items):
    """Puts each list element in its own list.

    Example:
        Input: [a, b, c]
        Output: [[a], [b], [c]]

    This is needed for tabulate to print rows [a], [b], and [c].

    Args:
        * items: A list to listify.

    Returns:
        A list that contains elements that are listified.
    """
    output = []
    for item in items:
        item_list = []
        item_list.append(item)
        output.append(item_list)
    return output

def print_error(message):
    """Prints the given message using click.secho with fg='red'.

    Args:
        * message: A string to be printed.

    Returns:
        None.
    """
    click.secho(message, fg='red')
