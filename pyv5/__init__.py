"""The Catia base object is from which most other functionality derives. See examples for more information.

>>> from pyv5 import catia
>>> application = catia()
>>> documents = application.documents
>>>
>>> document = application.active_document
>>>
>>> documents.add('Part')
"""

from pyv5.base_interfaces.base_application import catia_application as catia
from pyv5.base_interfaces.context import CATIADocHandler

__all__ = ["catia", "CATIADocHandler"]
