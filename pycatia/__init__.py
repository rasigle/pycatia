"""The Catia base object is from which most other functionality derives. See examples for more information.

>>> from pycatia import catia
>>> application = catia()
>>> documents = application.documents
>>>
>>> document = application.active_document
>>>
>>> documents.add('Part')
"""

from pycatia.base_interfaces.base_application import catia_application as catia

__all__ = ["catia"]
