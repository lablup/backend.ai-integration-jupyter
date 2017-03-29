# Sorna Jupyter Kernel

Your Jupyter notebooks are running on the Sorna Cloud!


## Installation and Usage

First, grab your API keypair in [Sorna Cloud](https://cloud.sorna.io).

```sh
$ pip install jupyter sorna-jupyter-kernel
$ python -m sorna.integration.jupyter.install
$ export SORNA_ACCESS_KEY=...
$ export SORNA_SECRET_KEY=...
$ jupyter notebook
```

Then you will see Sorna kernels in the new notebook menu:

<p style="text-align:center"><img src="nbmenu-preview.png" width="300"></p>

More kernels will become available soon!


## Development

Add `--sys-prefix` argument to tell the installer to recognize editable
installation under your virtual environment.

```sh
$ python -m venv venv
$ source venv/bin/activate
$ pip install jupyter
$ pip install -e .  # editable installation
$ python -m sorna.integration.jupyter.install --sys-prefix
$ export SORNA_ACCESS_KEY=...
$ export SORNA_SECRET_KEY=...
$ jupyter notebook
```


## Uninstall

To list and uninstall existing kernelspecs registered to Jupyter, use
`jupyter-kernelspec` command.
