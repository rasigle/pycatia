from pathlib import Path

import pytest
from win32com.universal import com_error

from pycatia import catia
from pycatia.types.document import AnyDocument


class _LazyApplication:
    """Connect on first use so pytest collection does not start CATIA."""

    def __init__(self):
        self._application = None

    def _get(self):
        if self._application is None:
            self._application = catia()
        return self._application

    def __getattr__(self, name):
        return getattr(self._get(), name)

    def __repr__(self):
        return repr(self._get())


application = _LazyApplication()


@pytest.fixture(scope="session")
def ensure_source_catia_files():
    """Create gitignored CATIA source documents once, after collection."""
    from tests.source_files import ensure_source_catia_files as _ensure

    _ensure()



def open_document(file_name: Path) -> AnyDocument:
    documents = application.documents
    # if the document is already open swtich to it's Window
    if file_name.name in [document.name for document in documents]:
        # the document maybe loaded but not have a window
        windows = application.windows
        if file_name.name in [window.name for window in windows]:
            document_window = windows.item(file_name.name)
            document_window.activate()
        else:
            documents.open(file_name)
    else:
        documents.open(file_name)

    document = application.active_document

    return document


def close_all():
    documents = application.documents
    try:
        for document in documents:
            document.close()
    except com_error:
        application.logger.warning("Could not close document.")


@pytest.fixture
def document_open(file_name: Path, ensure_source_catia_files):
    open_document(file_name)


# typically used for the last test within a module or if a change has been
# made that might break later tests.
@pytest.fixture
def document_open_test_close_all(file_name: Path, ensure_source_catia_files):
    open_document(file_name)
    yield
    close_all()


# typically used for the first test within a module
@pytest.fixture
def document_close_all_open(file_name: Path, ensure_source_catia_files):
    close_all()
    open_document(file_name)


@pytest.fixture
def document_close_all_open_test_close(file_name: Path, ensure_source_catia_files):
    documents = application.documents
    try:
        for document in documents:
            document.close()
    except com_error:
        application.logger.warning("Couuld not close document.")
    document = open_document(file_name)
    yield
    document.close()


@pytest.fixture
def document_open_test_close(file_name: Path, ensure_source_catia_files):
    document = open_document(file_name)
    yield
    document.close()
