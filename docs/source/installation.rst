.. _installation:

Installation
============

Use `uv <https://docs.astral.sh/uv/>`_ to install Python dependencies. A virtual
environment is created for you.

The Short Version
-----------------

This assumes Python 3.9 or later is already installed.

You can install pyv5 from PyPI or clone the repository from GitHub.

pypi
~~~~

To install from `PyPI <https://pypi.org/>`_::

    uv add pyv5

To upgrade the installed version::

    uv add pyv5 --upgrade

github
~~~~~~

To get the latest master version from GitHub::

    git clone https://github.com/rasigle/pyv5.git
    cd pyv5
    uv sync

``uv sync`` installs the project in editable mode together with the docs and
test extras and the ``dev`` dependency group defined in ``pyproject.toml``.


Registering the CATIA V5 COM server.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Typically, installing CATIA V5 will do this automatically as a part of the
installation process. However, sometimes that can fail.

1. From the command prompt navigate to the installation folder that contains
cnext.exe of the CATIA V5 installation you would like to register. For example::

    cd <drive>\<CATIA_DIR>\<CATIA_VERSION>\code\bin


2. run the following command after replacing <env_file> and <path_to_env_file>
with the appropriate values::

    cnext.exe /regserver -env <env_file> -direnv <path_to_env_file>


Now for an :ref:`introduction` to pyv5.
