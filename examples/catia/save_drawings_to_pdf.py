# author: evereux
# contact: evereux@gmail.com

"""
Save Drawings To PDF

Description
===========
Loops through all the files (.CATDrawing) of a given directory and saves to
PDF.

For CATDrawings the Document.export_data() method exports each sheet to a
single PDF. This script uses pypdf to merge these single sheets into a
single pdf for each drawing.

Requirements
============
python >= 3.9
pyv5 >= 0.6.4
pypdf
CATIA V5 running
A network accessible folder that contain your CATDrawings.

Documentation
=============
https://pyv5.readthedocs.io

More examples and user scripts can be found at:
https://github.com/evereux/pyv5/tree/master/examples
https://github.com/evereux/pyv5/tree/master/user_scripts
"""

from pathlib import Path

from pypdf import PdfWriter

from pyv5 import CATIADocHandler
from pyv5.interfaces.drafting.drawing_document import DrawingDocument

exclude_strings = ["Detail", "DXF"]
source_cat_drawings = Path(Path.home(), "catia_parts")
save_path = Path(Path.home(), "Pictures", "catia_pdfs")

drawing_file_names = []

for f in source_cat_drawings.glob("*.CATDrawing"):
    with CATIADocHandler(file_name=f) as handler:
        caa = handler.application
        part_document = handler.document
        drawing = DrawingDocument(part_document.com_object)
        pdf_name = Path(save_path, drawing.name).with_suffix(".pdf")
        drawing.export_data(pdf_name, "pdf", overwrite=True)
        drawing_file_names.append(drawing.name)

delete_files = []
for fn in drawing_file_names:
    merger = PdfWriter()
    # get all the PDFS that start with drawing file name (without suffix).
    s = fn.split(".CATDrawing")[0]
    files = sorted(save_path.glob(f"{s}*.*"))
    pdf_name = Path(save_path, f"{s}.pdf")
    for pdf in files:
        # don't merge files whose name has text that appears in exclude_strings
        r = [i for i in exclude_strings if (i in str(pdf))]
        if len(r) == 0:
            merger.append(pdf)
        delete_files.append(pdf)
    merger.write(pdf_name)
    merger.close()

# delete the single sheets.
for f in delete_files:
    f.unlink()
