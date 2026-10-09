"""

Example - Shape Factory - 002

Description:
    Mirror the main body of the part.

Requirements:
    - CATIA running with an open part with an non-empty main body.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################

from pyv5 import v5
from pyv5.interfaces.mec_mod.part_document import PartDocument

application = v5()
# if the active document is a CATPart this will return a PartDocument
part_document: PartDocument = application.active_document
part = part_document.part
part.in_work_object = part.main_body

mirror_reference = part.create_reference_from_object(part.origin_elements.plane_zx)
shape_factory = part.shape_factory
mirror_symmetry = shape_factory.add_new_symmetry_2(mirror_reference)

part.in_work_object = part.main_body
part.update_object(part.main_body)
