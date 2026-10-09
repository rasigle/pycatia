"""

Example - Document - 003

Description:
    Opens a CATIA fila and exports it as STEP. Then closes the file.

Requirements:
    - CATIA running.
    - Tests already setup.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################

import os
from pathlib import Path

from pyv5 import v5
from pyv5.interfaces.mec_mod.part_document import PartDocument

# path to file to open.
file_name = Path(Path(os.getcwd()).parent, r"tests\assets\part_measurable.CATPart")

application = v5()
# open document
documents = application.documents
part_document: PartDocument = documents.open(file_name)

assert isinstance(part_document, PartDocument)

# _Full_ path of new file. This uses current working directory.
new_file_name = Path(os.getcwd(), "new_part.CATPart")
# save document as new name.
part_document.save_as(new_file_name, overwrite=True)

# to export to another support file_format (license permitting).
new_export_file_name = Path("c:\\temp\\new_export_part.stp")
part_document.export_data(new_export_file_name, "stp", overwrite=True)

# close document
part_document.close()
