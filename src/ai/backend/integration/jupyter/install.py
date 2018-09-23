'''
The kernel installer.

Run `python -m ai.backend.integration.jupyter.install` to use Backend.AI in your Jupyter notebooks.
'''

import argparse
import json
import os
import sys
import webbrowser

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory
from .kernel import kernels


def clean_kernel_spec(user=True, prefix=None):
    mgr = KernelSpecManager()
    # NOTE: remove_kernel_spec() and get_all_specs() does not support explicit prefix.
    #       Sometimes we may need to perform --clean-only multiple times to completely
    #       remove all kernelspecs installed around venvs and system global directories.
    for name, info in mgr.get_all_specs().items():
        if name.startswith('backend'):
            print("Removing existing Backend.AI kernel: {0}"
                  .format(info['spec']['display_name']))
            mgr.remove_kernel_spec(name)


def install_kernel_spec(name, spec_json, user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(spec_json, f, sort_keys=True)
        print("Installing Backend.AI Jupyter kernel spec: {0}"
              .format(spec_json['display_name']))
        KernelSpecManager().install_kernel_spec(
            td, name, user=user, replace=True, prefix=prefix)


def query_yes_no(prompt):
    valid = {'y': True, 'yes': True, 'n': False, 'no': False}
    while True:
        choice = input('{0} [y/n] '.format(prompt)).lower()
        if choice in valid:
            return valid[choice]
        else:
            prompt = 'Pleas answer in y/yes/n/no.'


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
    ap.add_argument('--clean-only', action='store_true',
        help="Perform only clean-up of existing Backend.AI kernels.")
    ap.add_argument('-q', '--quiet', action='store_true',
        help="Do not ask the user anything.")
    ap.add_argument('--prefix',
        help="Install to the given prefix. "
             "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/")
    args = ap.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True

    clean_kernel_spec(user=args.user, prefix=args.prefix)
    if args.clean_only:
        return

    for kern in kernels:
        spec = {
            "argv": [sys.executable, "-m", "ai.backend.integration.jupyter",
                     "-f", "{connection_file}",
                     "--",
                     "-k", kern.__name__],
            "display_name": kern.language_info['name'],
            "language": kern.language,
        }
        install_kernel_spec(kern.__name__, spec, user=args.user, prefix=args.prefix)

    if not args.quiet:
        print()
        has_api_key = bool(os.environ.get('BACKEND_ACCESS_KEY', ''))
        if has_api_key:
            print('It seems that you already configured the API key. Enjoy!')
        else:
            if query_yes_no('You can get your own API keypair from https://cloud.backend.ai. Do you want to open the site?'):
                webbrowser.open_new_tab('https://cloud.backend.ai')
            print()
            print('If you already have the keypair or just grabbed a new one,')
            print('run the following in your shell before running jupyter notebook:\n')
            print('  export BACKEND_ACCESS_KEY="AKIA..."')
            print('  export BACKEND_SECRET_KEY="......."\n')


if __name__ == '__main__':
    main()
