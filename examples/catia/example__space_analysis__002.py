"""

Example - Space Analysis - 002

Description:
    Get all the points in the geometrical set 'Points' and output co-ordinate to console.
    Create your own CATPart with a Geometrical Set called construction_points.
    Add some points to the Geometrical Set.

Requirements:
    - A part document with the above described setup.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################
from pathlib import Path

from pyv5 import v5
from pyv5.interfaces.mec_mod.hybrid_body import HybridBody
from pyv5.interfaces.mec_mod.part_document import PartDocument

application = v5()
documents = application.documents
# this should be the path to your file.
# if the active document is a CATPart this will return a PartDocument
part_document: PartDocument = documents.open(
    Path(os.getcwd(), r"tests\assets\part_measurable.CATPart")
)
part = part_document.part
spa_workbench = part_document.spa_workbench()

hybrid_bodies = part.hybrid_bodies
hybrid_body_item = hybrid_bodies.get_item_by_name("construction_points")
assert hybrid_body_item is not None
hybrid_body = HybridBody(hybrid_body_item.com_object)

shapes = hybrid_body.hybrid_shapes

for point in shapes:
    reference = part.create_reference_from_object(point)
    measurable = spa_workbench.get_measurable(reference)
    coordinates = measurable.get_point()
    print(f"{point.name}: {coordinates}")
