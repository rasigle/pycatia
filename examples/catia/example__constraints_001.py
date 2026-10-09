"""

Example - Constraints - 001

Description:
    Fix the first Sub Product in Product using constraints.
    The Sketch examples also show further usage of constraints.

Requirements:
    - An open product document with at least two parts inside.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################

from pyv5 import CatConstraintType, v5
from pyv5.interfaces.product_structure.product_document import ProductDocument

application = v5()
# if the active document is a CATProduct this will return a ProductDocument
product_document: ProductDocument = application.active_document
product = product_document.product

products = product.products
constraints = product.constraints()
sub_prod_1 = products.item(1)
ref_sub_prod_1 = sub_prod_1.reference_product

sub_prod_1_name = f"{product.name}/{sub_prod_1.name}/!{product.name}/{sub_prod_1.name}/"
reference = product.create_reference_from_name(sub_prod_1_name)

constraints.add_mono_elt_cst(CatConstraintType.catCstTypeReference, reference)
