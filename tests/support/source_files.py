from tests.support.common_vars import test_files

# Paths only. CATPart/CATProduct/CATDrawing files are gitignored and created on
# the first test run (see ensure_source_catia_files in conftest). Do not call
# the create_source helpers at import time: pytest collection imports this
# module, and generating those documents in CATIA blocks "instantiating tests".
design_table_1 = test_files / "design_table_1.txt"
cat_drawing = test_files / "drawing.CATDrawing"
cat_part_measurable = test_files / "part_measurable.CATPart"
cat_product = test_files / "product_top.CATProduct"
cat_functional_system = test_files / "FunctionalSystem1.CATSystem"
igs_file = test_files / "part_measurable.igs"
stp_file = test_files / "part_measurable.stp"


def __getattr__(name: str):
    # Catalog.CATMaterial lives in the CATIA install, not this repo.
    if name == "cat_material":
        from tests.support.create_source_material import get_cat_material

        return get_cat_material()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def ensure_source_catia_files() -> None:
    from tests.support.create_source_drawing import get_cat_drawing
    from tests.support.create_source_functional_system import get_cat_functional_system
    from tests.support.create_source_parts import get_cat_part_measurable
    from tests.support.create_source_products import get_cat_product_top

    get_cat_part_measurable()
    get_cat_product_top()
    get_cat_drawing()
    get_cat_functional_system()
