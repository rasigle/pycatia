from typing import TYPE_CHECKING, TypeVar

#: CATVariant The CATVariant type allows both int and string.
CATVariant = int | str

list_str = TypeVar("list_str", list, str)

if TYPE_CHECKING:
    from pyv5.interfaces.analysis.analysis_document import AnalysisDocument
    from pyv5.interfaces.cat_mat.material_document import MaterialDocument
    from pyv5.interfaces.core.document import Document
    from pyv5.interfaces.dmaps.process_document import ProcessDocument
    from pyv5.interfaces.drafting.drawing_document import DrawingDocument
    from pyv5.interfaces.funct_system.functional_document import FunctionalDocument
    from pyv5.interfaces.knowledge.bool_param import BoolParam
    from pyv5.interfaces.knowledge.free_parameter import FreeParameter
    from pyv5.interfaces.knowledge.int_param import IntParam
    from pyv5.interfaces.knowledge.list_parameter import ListParameter
    from pyv5.interfaces.knowledge.parameter import Parameter
    from pyv5.interfaces.knowledge.real_param import RealParam
    from pyv5.interfaces.knowledge.str_param import StrParam
    from pyv5.interfaces.mec_mod.part_document import PartDocument
    from pyv5.interfaces.product_structure.product_document import ProductDocument

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
        | MaterialDocument
        | ProcessDocument
        | Document
        | DrawingDocument
        | FunctionalDocument
        | PartDocument
        | ProductDocument
    )

    document_types: dict

# Document and parameter classes import CATVariant from this module, so those
# unions are resolved on first access instead of at import time.
_LAZY_NAMES = frozenset({"AnyParameter", "AnyDocument", "document_types"})


def _load_parameter_types() -> None:
    global AnyParameter
    if "AnyParameter" in globals():
        return

    from pyv5.interfaces.knowledge.bool_param import BoolParam
    from pyv5.interfaces.knowledge.free_parameter import FreeParameter
    from pyv5.interfaces.knowledge.int_param import IntParam
    from pyv5.interfaces.knowledge.list_parameter import ListParameter
    from pyv5.interfaces.knowledge.parameter import Parameter
    from pyv5.interfaces.knowledge.real_param import RealParam
    from pyv5.interfaces.knowledge.str_param import StrParam

    AnyParameter = (
        BoolParam
        | FreeParameter
        | IntParam
        | ListParameter
        | Parameter
        | RealParam
        | StrParam
    )


def _load_document_types() -> None:
    global AnyDocument, document_types
    if "document_types" in globals():
        return

    _load_parameter_types()

    from pyv5.interfaces.analysis.analysis_document import AnalysisDocument
    from pyv5.interfaces.cat_mat.material_document import MaterialDocument
    from pyv5.interfaces.components_catalogs.catalog_document import CatalogDocument
    from pyv5.interfaces.core.document import Document
    from pyv5.interfaces.dmaps.process_document import ProcessDocument
    from pyv5.interfaces.drafting.drawing_document import DrawingDocument
    from pyv5.interfaces.funct_system.functional_document import FunctionalDocument
    from pyv5.interfaces.mec_mod.part_document import PartDocument
    from pyv5.interfaces.product_structure.product_document import ProductDocument

    AnyDocument = (
        AnalysisDocument
        | MaterialDocument
        | ProcessDocument
        | Document
        | DrawingDocument
        | FunctionalDocument
        | PartDocument
        | ProductDocument
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


def __getattr__(name: str):
    if name == "AnyParameter":
        _load_parameter_types()
        return AnyParameter
    if name in {"AnyDocument", "document_types"}:
        _load_document_types()
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | _LAZY_NAMES)
