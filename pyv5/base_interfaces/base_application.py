#! /usr/bin/python3.9

import pythoncom
from pywintypes import com_error
from win32com.client import Dispatch, GetActiveObject

from pyv5.exception_handling.exceptions import CATIAApplicationException
from pyv5.in_interfaces.application import Application

COM_APPLICATION_NAMES = (
    "CATIA.Application",
    "DELMIA.Application",
    "CNEXT.Application",
)


def catia_application(co_initialise=False) -> Application:
    """
    Connect to a CATIA, DELMIA or CNEXT COM application.

    GetActiveObject is tried for each known application name so a running
    DELMIA or CNEXT session is found even when CATIA.Application is not
    registered. The first running instance is returned. If none are running,
    Dispatch is tried in the same order so an installed application can still
    be started.
    """
    if co_initialise:
        pythoncom.CoInitialize()

    last_error = None
    for com_name in COM_APPLICATION_NAMES:
        try:
            return Application(GetActiveObject(com_name))
        except com_error as err:
            last_error = err

    for com_name in COM_APPLICATION_NAMES:
        try:
            return Application(Dispatch(com_name))
        except com_error as err:
            last_error = err

    raise CATIAApplicationException(
        "Could not connect to CATIA.Application, DELMIA.Application or CNEXT.Application."
    ) from last_error
