"""
Module initially auto generated using V5Automation files from CATIA V5 R28 on
2020-09-25 14:34:21.593357

.. warning::
    The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
    They are there as a guide as to how the Visual Basic / catscript functions work
    and thus help debugging in pyv5.

"""

from pyv5.base.types import CATVariant
from pyv5.interfaces.product_structure.product import Product
from pyv5.interfaces.system.collection import Collection


class PPRProducts(Collection):
    """
    .. note::
        :class: toggle

        CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)

            | System.IUnknown
            |     System.IDispatch
            |         System.CATBaseUnknown
            |             System.CATBaseDispatch
            |                 System.Collection
            |                     PPRProducts
            |
            | This interface is used to retrieve and add Products from and to the list of
            | Products.

    """

    def __init__(self, com_object):
        super().__init__(com_object, child_object=Product)
        self.ppr_products = com_object

    def add(self, i_product: Product) -> Product:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Func Add(Product iProduct) As Product
                |
                |     Adds the specified Product to the current list of
                |     Products.
                |
                |     Parameters:
                |
                |         iProduct
                |             The Product to be added.
                |
                |     Returns:
                |         The added Product.

        :param Product i_product:
        :rtype: Product
        """
        return Product(self.ppr_products.Add(i_product.com_object))

    def item(self, i_index: CATVariant) -> Product:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Func Item(CATVariant iIndex) As Product
                |
                |     Retrieves the Product corresponding to the specified index in the list of
                |     Products.
                |
                |     Parameters:
                |
                |         iIndex
                |             The index in the Product list.
                |
                |     Returns:
                |         The retrieved Product corresponding to the specified index.

        :param CATVariant i_index:
        :rtype: Product
        """
        return Product(self.ppr_products.Item(i_index))

    def __repr__(self):
        return f'PprProducts(name="{self.name}")'
