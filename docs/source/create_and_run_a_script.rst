.. _create_and_run_a_script:

Create And Run A Script
=======================

The process of creating and running python scripts can be executed a number of
different ways. The following will just explain the basics.

* In your pyv5-scripts folder `c:\Users\<username>\python\pyv5-scripts` create
  a new file called `catia_details.py`.


* Open and edit this file in your favourite file text editor (not MS Word etc!) / IDE
  (eg VS Code / pycharm) and write the following:


.. code-block:: python

    from pyv5 import v5

    application = v5()

    full_name = application.full_name
    sys_config = application.system_configuration
    release = sys_config.release
    version = sys_config.version
    service_pack = sys_config.service_pack

    print(f'''
    You are currently running CATIA V{version} release {release} SP {service_pack}.
    ''')


* Save the file in your editor.

* Open a terminal and navigate to your pyv5-scripts folder.

.. code-block::

   cd c:\Users\<username>\python\pyv5-scripts

* Run the script with uv:

.. code-block::

    uv run python catia_details.py

The script should then display the following:

.. code-block::

    You are currently running CATIA V5 release XX SP XXX

For more detailed examples on how to interact with pyv5 see the
:ref:`examples` page. There contain several scripts that can be run in the
terminal.
