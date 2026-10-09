#! /usr/bin/python3.9

import os
from datetime import datetime
from pathlib import Path

import pytest
from pywintypes import com_error

from pyv5.base_interfaces.context import CATIADocHandler
from pyv5.in_interfaces.document import Document
from pyv5.mec_mod_interfaces.part_document import PartDocument
from pyv5.product_structure_interfaces.product_document import ProductDocument
from pyv5.types.document import document_types
from tests.conftest import application
from tests.source_files import cat_part_measurable
from tests.source_files import cat_product
from tests.source_files import stp_file
from tests.source_files import igs_file

junk_folder = os.path.join(os.getcwd(), "__junk__/")
now_string = datetime.now().strftime("%Y%m%d-%H%M%S")
os.makedirs(junk_folder, exist_ok=True)

igs_file_param = pytest.param(
    igs_file,
    marks=pytest.mark.skipif(not igs_file.is_file(), reason="part_measurable.igs is not available")
)
stp_file_param = pytest.param(
    stp_file,
    marks=pytest.mark.skipif(not stp_file.is_file(), reason="part_measurable.stp is not available")
)


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_activate_document(document_close_all_open):
    documents = application.documents
    doc_1 = application.active_document
    doc_2 = documents.open(cat_product)

    documents


def test_add_document():
    documents = application.documents
    required_types = ("Part", "Product")
    optional_types = (
        "Analysis",
        "CatalogDocument",
        "Drawing",
        "CATProcess",
        "FeatureDictionary",
    )

    def add_document(document_type: str, required: bool):
        try:
            document = documents.add(document_type)
        except com_error:
            if required:
                raise
            return
        assert document_types[document_type]["extension"] in document.name
        document.close()

    for document_type in required_types:
        add_document(document_type, required=True)
    for document_type in optional_types:
        add_document(document_type, required=False)


@pytest.mark.parametrize('file_name', [cat_product])
def test_count_types(document_open):
    documents = application.documents
    num = documents.count_types(".CATPart")
    assert num == 1


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_export_document(document_open):
    document = application.active_document
    assert document is not None

    export_type = "stl"
    export_path = Path(cat_part_measurable).resolve().parent / f"export_file.{export_type}"
    if export_path.is_file():
        export_path.unlink()

    try:
        document.export_data(export_path, export_type)
    except com_error:
        pytest.skip(f"{export_type} export is not available in this CATIA session.")

    assert export_path.is_file()
    export_path.unlink()


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_full_name(document_open):
    """
    :return:
    """
    document = application.active_document
    assert document is not None
    assert str(cat_part_measurable) == document.full_name


def test_get_documents_names():
    pass
    # todo: update this test so that's more reliable. currently get_item_names()
    # can return additional documents held open by CATIA.
    #
    # with CATIADocHandler(cat_product) as caa_:
    #     documents = caa_.documents
    #
    #     expected_names = [
    #         "product_top.CATProduct",
    #         "product_sub_2.CATProduct",
    #         "part_measurable.CATPart",
    #         "product_sub_1.CATProduct",
    #     ]
    #
    #     assert expected_names in documents.get_item_names()


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_is_saved(document_open_test_close):
    document = application.active_document
    assert document is not None
    assert document.is_saved

    part = PartDocument(document.com_object).part

    # create a new geometrical set to add point.
    geometrical_set = part.hybrid_bodies.add()
    geometrical_set.name = "lalalalalala"

    # just adding geometrical set isn't enough to trigger is_saved to be False
    # catia r21 bug?
    # so a new point is also added.
    factory = part.hybrid_shape_factory
    point = factory.add_new_point_coord(0, 1, 2)
    geometrical_set.append_hybrid_shape(point)
    part.update()

    assert not document.is_saved


@pytest.mark.parametrize('file_name', [cat_product])
def test_item(document_open_test_close):
    documents = application.documents
    doc_com1 = documents.item(cat_product.name)

    assert doc_com1.name == cat_product.name


def test_new_from():
    documents = application.documents
    document = documents.new_from(cat_part_measurable)
    assert document.name is not os.path.basename(cat_part_measurable)
    document.close()


def test_new_from_str():
    documents = application.documents
    document = documents.new_from(str(cat_part_measurable))
    assert document.name is not os.path.basename(cat_part_measurable)
    document.close()


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_open_document(document_open_test_close):
    part_document: PartDocument = application.active_document
    assert type(part_document) is PartDocument


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_open_document_str(document_open_test_close):
    part_document: PartDocument = application.active_document
    assert type(part_document) is PartDocument


@pytest.mark.parametrize('file_name', [igs_file_param])
def test_open_document_igs(document_open_test_close):
    document = application.active_document
    assert type(document) is PartDocument


@pytest.mark.parametrize('file_name', [stp_file_param])
def test_open_document_stp(document_open_test_close):
    document = application.active_document
    assert type(document) is PartDocument


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_read_document(document_open_test_close):
    document = application.active_document
    assert type(document) is PartDocument


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_read_document_strget_application(document_open_test_close):
    document = application.active_document
    assert type(document) is PartDocument


@pytest.mark.parametrize('file_name', [igs_file_param])
def test_read_document_igs(document_open_test_close):
    document = application.active_document
    assert type(document) is PartDocument


@pytest.mark.parametrize('file_name', [stp_file_param])
def test_read_document_stp(document_open_test_close):
    document = application.active_document
    assert type(document) is PartDocument


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_part(document_open_test_close):
    part_document: PartDocument = application.active_document

    part = part_document.part
    assert part.name == "cat_part_measurable"
    assert part_document.is_part
    assert not part_document.is_product


@pytest.mark.parametrize('file_name', [cat_product])
def test_product(document_open_test_close):
    product_document: ProductDocument = application.active_document

    product = product_document.product
    assert "cat_product_1" in product.name


@pytest.mark.parametrize('file_name', [cat_part_measurable])
def test_saving(document_open_test_close):
    new_filename = Path(junk_folder, f"{now_string}.CATPart")

    part_document: PartDocument = application.active_document
    assert part_document is not None

    part_document.save_as(new_filename)
    part_document.save()

    assert os.path.isfile(new_filename)

    with pytest.raises(FileExistsError):
        part_document.save_as(new_filename)

    os.remove(new_filename)
