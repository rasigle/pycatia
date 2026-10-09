#
# Configuration file for the Sphinx documentation builder.
#
# http://www.sphinx-doc.org/en/master/config

from __future__ import annotations

import importlib.metadata
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

subprocess.check_call(
    [sys.executable, str(REPO_ROOT / "scripts" / "documentation" / "generate_api.py")],
)


class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = [
    "pywin32",
    "win32com",
    "win32com.client",
    "pywintypes",
    "pythoncom",
]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# -- Project information -----------------------------------------------------

project = "pyv5"
copyright = "2026, Paul Bourne"
author = "Paul Bourne"

version = importlib.metadata.version("pyv5")
release = version

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx_togglebutton",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = None

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_theme_options = {
    "logo": "pyv5-logo.png",
    "github_user": "evereux",
    "github_repo": "pyv5",
    "github_button": True,
}
html_static_path = ["_static"]
html_theme_path = []
html_css_files = [
    "css/pyv5.css",
]
htmlhelp_basename = "pyv5doc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
latex_documents = [
    (master_doc, "pyv5.tex", "pyv5 Documentation", "Paul Bourne", "manual"),
]

man_pages = [(master_doc, "pyv5", "pyv5 Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "pyv5",
        "pyv5 Documentation",
        author,
        "pyv5",
        "Python interface to the CATIA/DELMIA V5 COM API.",
        "Miscellaneous",
    ),
]

epub_title = project
epub_exclude_files = ["search.html"]

todo_include_todos = True
