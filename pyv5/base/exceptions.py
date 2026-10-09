class pyv5BaseException(Exception):
    """
    pyv5BaseException class.
    """

    pass


class CATIAApplicationException(pyv5BaseException):
    """ """

    def __init__(self, message):
        """

        :param message:
        """

        self.message = message
