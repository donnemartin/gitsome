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
