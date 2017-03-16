'''
The kernel installer.

Run `python -m sorna.integration.jupyter.install` to use Sorna in your Jupyter notebooks.
'''

import argparse
import json
import os
import sys

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory
from .kernel import sorna_kernels


def install_kernel_spec(name, spec_json, user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(spec_json, f, sort_keys=True)
        print(f"Installing Sorna-backed Jupyter kernel spec: {spec_json['display_name']}")
        KernelSpecManager().install_kernel_spec(
            td, name, user=user, replace=True, prefix=prefix)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False # assume not an admin on non-Unix platforms

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', action='store_true',
        help="Install to the per-user kernels registry. Default if not root.")
    ap.add_argument('--sys-prefix', action='store_true',
        help="Install to sys.prefix (e.g. a virtualenv or conda env)")
    ap.add_argument('--prefix',
        help="Install to the given prefix. "
             "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/")
    args = ap.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True

    for kern in sorna_kernels:
        spec = {
            "argv": [sys.executable, "-m", "sorna.integration.jupyter",
                     "-f", "{connection_file}",
                     "--",
                     "-k", kern.__name__],
            "display_name": kern.language_info['name'],
            "language": kern.language,
        }
        install_kernel_spec(kern.__name__, spec, user=args.user, prefix=args.prefix)

if __name__ == '__main__':
    main()
