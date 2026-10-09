"""

Example - Product - 006

Description:
    Get the Inertia of a product using product.get_technical object and print it's mass.
    See Inertia class for full list of properties and methods available.

Requirements:
    - An open part document.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################

from pyv5 import v5
from pyv5.interfaces.product_structure.product_document import ProductDocument
from pyv5.interfaces.space_analyses.inertia import Inertia

application = v5()
product_document: ProductDocument = application.active_document
product = product_document.product

inertia_com = product.get_technological_object("Inertia")
inertia = Inertia(inertia_com)

print(inertia.mass)
