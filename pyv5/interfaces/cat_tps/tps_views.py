#! usr/bin/python3.9
"""
Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-09-25 14:34:21.593357

.. warning::
    The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
    They are there as a guide as to how the visual basic / catscript functions work
    and thus help debugging in pyv5.

"""

from collections.abc import Iterator

from pyv5.interfaces.cat_tps.tps_view import TPSView
from pyv5.interfaces.system.collection import Collection
from pyv5.base.types import CATVariant


class TPSViews(Collection):
    """
    .. note::
        :class: toggle

        CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)

            | System.IUnknown
            |     System.IDispatch
            |         System.CATBaseUnknown
            |             System.CATBaseDispatch
            |                 System.Collection
            |                     TPSViews
            |
            | Interface for collection of TPS Views CATIATPSView.

    """

    def __init__(self, com_object):
        super().__init__(com_object, child_object=TPSView)
        self.tps_views = com_object

    def item(self, i_index: CATVariant) -> TPSView:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Func Item(CATVariant iIndex) As AnyObject
                |
                |     Retrieve a TPS View.

        :param CATVariant i_index:
        :rtype: AnyObject
        """
        return TPSView(self.tps_views.Item(i_index))

    def __getitem__(self, n: int) -> TPSView:
        if (n + 1) > self.count:
            raise StopIteration

        return TPSView(self.tps_views.Item(n + 1))

    def __iter__(self) -> Iterator[TPSView]:
        for i in range(self.count):
            yield self.child_object(self.com_object.Item(i + 1))

    def __repr__(self):
        return f'TpsViews(name="{self.name}")'
