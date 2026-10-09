from typing import TypeVar

from pyv5.interfaces.knowledge.bool_param import BoolParam
from pyv5.interfaces.knowledge.free_parameter import FreeParameter
from pyv5.interfaces.knowledge.int_param import IntParam
from pyv5.interfaces.knowledge.list_parameter import ListParameter
from pyv5.interfaces.knowledge.parameter import Parameter
from pyv5.interfaces.knowledge.real_param import RealParam
from pyv5.interfaces.knowledge.str_param import StrParam
from pyv5.interfaces.analysis.analysis_document import AnalysisDocument
from pyv5.interfaces.cat_mat.material_document import MaterialDocument
from pyv5.interfaces.components_catalogs.catalog_document import CatalogDocument
from pyv5.interfaces.dmaps.process_document import ProcessDocument
from pyv5.interfaces.drafting.drawing_document import DrawingDocument
from pyv5.interfaces.funct_system.functional_document import FunctionalDocument
from pyv5.interfaces.core.document import Document
from pyv5.interfaces.mec_mod.part_document import PartDocument
from pyv5.interfaces.product_structure.product_document import ProductDocument

#: CATVariant The CATVariant type allows both int and string.
CATVariant = int | str

list_str = TypeVar("list_str", list, str)

AnyParameter = (
    BoolParam
    | FreeParameter
    | IntParam
    | ListParameter
    | Parameter
    | RealParam
    | StrParam
)


AnyDocument = (
    AnalysisDocument
    | AnalysisDocument
    | MaterialDocument
    | ProcessDocument
    | Document
    | DrawingDocument
    | FunctionalDocument
    | PartDocument
    | ProductDocument
    | ProcessDocument
)

document_types = {
    "Analysis": {
        "extension": "CATAnalysis",
        "type": AnalysisDocument,
    },
    "CatalogDocument": {
        "extension": "catalog",
        "type": CatalogDocument,
    },
    "CATMaterial": {
        "extension": "CATMaterial",
        "type": MaterialDocument,
    },
    "CATProcess": {
        "extension": "CATProcess",
        "type": ProcessDocument,
    },
    "cgm": {
        "extension": "cgm",
        "type": Document,
    },
    "Drawing": {
        "extension": "CATDrawing",
        "type": DrawingDocument,
    },
    "FeatureDictionary": {"extension": "CATfct", "type": Document},
    "gl": {
        "extension": "gl",
        "type": Document,
    },
    "gl2": {
        "extension": "gl2",
        "type": Document,
    },
    "hpgl": {"extension": "hpgl", "type": Document},
    "FunctionalSystem": {
        "extension": "CATSystem",
        "type": FunctionalDocument,
    },
    "Part": {
        "extension": "CATPart",
        "type": PartDocument,
    },
    "Product": {"extension": "CATProduct", "type": ProductDocument},
    "ProcessLibrary": {
        "extension": "act",
        "type": ProcessDocument,
    },
    "Default": {"extension": None, "type": Document},
}
