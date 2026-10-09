#! usr/bin/python3.9
"""
Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-09-25 14:34:21.593357

.. warning::
    The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
    They are there as a guide as to how the visual basic / catscript functions work
    and thus help debugging in pyv5.

"""
from typing import TYPE_CHECKING

from pyv5.interfaces.core.document import Document
from pyv5.interfaces.system.collection import Collection

if TYPE_CHECKING:
    from pyv5.base.types import CATVariant


class AnalysisLinkedDocuments(Collection):
    """
    .. note::
        :class: toggle

        CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)

            | System.IUnknown
            |     System.IDispatch
            |         System.CATBaseUnknown
            |             System.CATBaseDispatch
            |                 System.Collection
            |                     AnalysisLinkedDocuments
            |
            | The collection of Documents linked by Analysis.

    """

    def __init__(self, com_object):
        super().__init__(com_object, child_object=Document)
        self.analysis_linked_documents = com_object

    def item(self, i_index: CATVariant) -> Document:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Func Item(CATVariant iIndex) As Document
                |
                |     Returns a Document by its index or its name from the linked Documents
                |     collection.
                |
                |     Parameters:
                |
                |         iIndex
                |             The index or the name of the linked Document to retrieve from the
                |             collection of linked Documents. As a numerics, this index is the rank of the
                |             linked Document in the collection. The index of the first linked Document in
                |             the collection is 1, and the index of the last linked Document is Count. As a
                |             string, it is the name you assigned to the collection by using the
                |
                |
                |         AnyObject.Name property.
                |     Returns:
                |         The retrieved linked Document

        :param CATVariant i_index:
        :rtype: Document
        """
        return Document(self.analysis_linked_documents.Item(i_index))

    def __repr__(self):
        return f'AnalysisLinkedDocuments(name="{self.name}")'
