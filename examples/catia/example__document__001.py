"""

Example - Document - 001

Description:
    Use the context manager to open CATIA documents and close

Requirements:
    - CATIA running.
    - Tests already setup.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

from pyv5 import CATIADocHandler
from pyv5.interfaces.mec_mod.part_document import PartDocument

sys.path.insert(0, os.path.abspath("../../pyv5"))
##########################################################
import time
from pathlib import Path

catia_part = Path(Path(os.getcwd()).parent, r"tests\cat_files\part_measurable.CATPart")

with CATIADocHandler(catia_part) as caa:
    part_document: PartDocument = caa.document
    # do some stuff.
    # save if you need to.
    time.sleep(5)  # don't do this, no need.
    # document is automatically closed. Lovely.
