Backend.AI Integration for Jupyter
==================================

Your Jupyter notebooks are running on the Backend.AI Cloud!

Migration Guide for v0.1.x "Sorna" Users
----------------------------------------

Now we use the v1.0.0 release of `Backend.AI Client for Python
<https://pypi.python.org/pypi/backend.ai-client>`.

To use the latest version, please remove all existing "Sorna" kernel
configurations and re-install them.

.. code-block:: console

   $ python -m sorna.integration.jupyter.install --clean-only
   Removing existing Sorna kernel: C11 on Sorna
   ...

   $ pip uninstall sorna-jupyter-integration
   ...

   $ pip install backend.ai-integration-jupyter
   ...

   $ python -m ai.backend.integration.jupyter.install
   Installing Backend.AI Jupyter kernel spec: Python 3 on Backend.AI
   ...

Note that you also need to reconfigure your existing notebooks to use the new
kernels.  This is a safe operation -- you can change the backend kernel without
losing/modifying the content of notebooks.


Installation and Usage
----------------------

First, grab your API keypair in `Backend.AI Cloud <https://cloud.backend.ai>`_.

.. code-block:: console

   $ pip install jupyter backend.ai-integration-jupyter
   $ python -m ai.backend.integration.jupyter.install
   $ export BACKEND_ACCESS_KEY=...
   $ export BACKEND_SECRET_KEY=...
   $ jupyter notebook

Then you will see Backend.AI kernels in the new notebook menu:

.. image:: nbmenu-preview.png

More kernels will become available soon!


Development
-----------

Add ``--sys-prefix`` argument to tell the installer to recognize editable
installation under your virtual environment.

.. code-block:: console

   $ python -m venv venv
   $ source venv/bin/activate
   $ pip install jupyter
   $ pip install -e .  # editable installation
   $ python -m ai.backend.integration.jupyter.install --sys-prefix
   $ export BACKEND_ACCESS_KEY=...
   $ export BACKEND_SECRET_KEY=...
   $ jupyter notebook


Uninstall
---------

To list and uninstall existing kernelspecs registered to Jupyter, use
``jupyter-kernelspec`` command.
