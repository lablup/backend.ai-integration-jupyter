# sorna-jupyter-kernel
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
