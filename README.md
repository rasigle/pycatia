# pyv5 - providing Python access to the V5 COM API

An easy-to-use Python interface to the CATIA V5 and DELMIA V5 COM automation API.
It's based on the work of [pycatia](https://github.com/evereux/pycatia) by Paul Bourne.

pyv5 connects to a running V5 session and exposes the automation object model as Python classes. Scripts can create documents, navigate products, and drive workbenches through those objects.

## Overview

- Give Python a first-class way to automate CATIA V5 and DELMIA V5 on Windows.
- Connect to a running or start a new V5 session.
- Wrap the COM object model in typed Python classes with names that follow the V5 API.
- Provide helpers for document lifecycle, enumerations, and optional COM object arguments.
- Stay useful for production automation of parts, products, drawings, manufacturing, and robotics.

The generated wrappers cover a large share of the V5 automation interfaces. 
They are autocreated and updated using the V5 API documentation. 

Coverage and tests are strongest on the workbenches used in the examples and the test suite.

## Requirements

- Windows
- Python 3.9 or later
- CATIA V5 or DELMIA V5 installed and licensed
- Dependencies: [pywin32](https://pypi.org/project/pywin32/)

## Installation

Clone the repository and install into a virtual environment.

With [uv](https://docs.astral.sh/uv/):

```powershell
uv sync
```

For development (tests, docs, linters):

```powershell
uv sync --group dev
```

Start CATIA or DELMIA before you run scripts. pyv5 talks to the COM server of a live V5 session.

## Quick start

```python
from pyv5 import v5

application = v5()
documents = application.documents
part_document = documents.add("Part")

part = part_document.part
geom_set = part.hybrid_bodies.add()
geom_set.name = "Construction Geometry"
```

`v5()` looks for a running `CATIA.Application`, `DELMIA.Application`, or `CNEXT.Application`, then starts one if none is found.

Use `CATIADocHandler` as a contextmanager when you want a document opened or created and closed automatically:

```python
from pyv5 import CATIADocHandler

with CATIADocHandler(new_document="Part") as handler:
    document = handler.document
    # work with the document
```

## Documentation

- Sphinx sources: [`docs/source`](docs/source)
- Runnable examples: [`examples/catia`](examples/catia) and [`examples/delmia`](examples/delmia)
- API reference: build the docs locally with `docs/source/make.bat html`
- Changes: [`CHANGELOG.md`](CHANGELOG.md)

## Development

Integration tests expect a running V5 session with no documents open.

```powershell
pytest -v tests
```

In CATIA, disable the CGR cache and “activate default shapes on open”, and do not surround parameter names with backticks.

The first test run creates the CATIA files it needs under `tests/assets`. Delete those generated files if a later run fails in an unexpected way and you want them rebuilt.

## License

MIT. See [LICENSE.txt](LICENSE.txt).
