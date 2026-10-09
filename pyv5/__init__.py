"""The Catia base object is from which most other functionality derives. See examples for more information.

>>> from pyv5 import v5
>>> application = v5()
>>> documents = application.documents
>>>
>>> document = application.active_document
>>>
>>> documents.add('Part')
"""

from pyv5.base.base_application import v5_application as v5
from pyv5.base.context import CATIADocHandler
from pyv5.base.enums import *  # noqa: F403
from pyv5.base.enums import __all__ as _enum_all
from pyv5.base.nothing import vba_nothing

__all__ = ["v5", "CATIADocHandler", "vba_nothing", *_enum_all]
