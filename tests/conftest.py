import contextlib
import threading
from pathlib import Path

import pytest
import win32api
import win32con
import win32gui
import win32process
from win32com.universal import com_error

from pyv5.base.base_application import v5_application
from pyv5.base.types import AnyDocument

_CATIA_PROCESS_NAMES = {"cnext.exe", "delmia.exe", "catia.exe"}
_OK_BUTTON_LABELS = {"OK", "Ok", "&OK"}


def _pid_is_catia(pid: int) -> bool:
    try:
        handle = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
            False,
            pid,
        )
    except Exception:
        return False
    try:
        image = win32process.GetModuleFileNameEx(handle, 0)
    except Exception:
        return False
    finally:
        win32api.CloseHandle(handle)
    return Path(image).name.lower() in _CATIA_PROCESS_NAMES


def dismiss_catia_error_dialogs() -> None:
    """Click OK on modal CATIA error boxes so COM calls can return."""

    def _enum_window(hwnd, _):
        try:
            if win32gui.GetClassName(hwnd) != "#32770":
                return True
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if not _pid_is_catia(pid):
                return True

            def _enum_child(child, __):
                if (
                    win32gui.GetClassName(child) == "Button"
                    and win32gui.GetWindowText(child) in _OK_BUTTON_LABELS
                ):
                    win32gui.PostMessage(child, win32con.BM_CLICK, 0, 0)
                return True

            win32gui.EnumChildWindows(hwnd, _enum_child, None)
        except Exception:
            pass
        return True

    with contextlib.suppress(Exception):
        win32gui.EnumWindows(_enum_window, None)


@pytest.fixture(scope="session", autouse=True)
def _dismiss_catia_error_dialogs():
    stop = threading.Event()

    def _run():
        while not stop.wait(0.2):
            dismiss_catia_error_dialogs()

    thread = threading.Thread(target=_run, name="dismiss-catia-dialogs", daemon=True)
    thread.start()
    yield
    stop.set()
    thread.join(timeout=1.0)


class _LazyApplication:
    """Connect on first use so pytest collection does not start CATIA."""

    def __init__(self):
        self._application = None

    def _get(self):
        if self._application is None:
            self._application = v5_application()
            # Modal save/open dialogs freeze pytest waiting for a click.
            self._application.display_file_alerts = False
        return self._application

    def __getattr__(self, name):
        return getattr(self._get(), name)

    def __repr__(self):
        return repr(self._get())


application = _LazyApplication()


@pytest.fixture(scope="session")
def ensure_source_catia_files():
    """Create gitignored CATIA source documents once, after collection."""
    from tests.support.source_files import ensure_source_catia_files as _ensure

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
    application.display_file_alerts = False
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
    close_all()
    document = open_document(file_name)
    yield
    document.close()


@pytest.fixture
def document_open_test_close(file_name: Path, ensure_source_catia_files):
    document = open_document(file_name)
    yield
    document.close()
