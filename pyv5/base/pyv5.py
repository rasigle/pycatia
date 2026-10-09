import logging

from pyv5.base.cat_logger import create_logger


class PyV5:
    """
    Base class for the V5 application.
    """

    @property
    def logger(self) -> logging.Logger:
        """
        :rtype: logging.Logger
        """
        return create_logger()

    def release_check(self, current: int, required: int, name: str):
        """

        Used to notify user if the CATIA V5 version is lower than that required.

        :param int current:
        :param int required:
        :param str name:
        """
        if current < required:
            self.logger.info(
                f'"{name}" was introduced in R{required}. You are running R{current}.'
            )

    def __repr__(self):
        return "pyv5()"
