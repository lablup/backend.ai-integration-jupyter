from setuptools import setup
from pathlib import Path


setup(
    name='sorna-jupyter-kernel',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.3',
    description='Sorna Jupyter Kernel Integration',
    long_description=Path('README.rst').read_text(),
    url='https://github.com/lablup/sorna-jupyter-kernel',
    author='Lablup Inc.',
    author_email='joongi@lablup.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],

    packages=['sorna.integration.jupyter'],
    namespace_packages=['sorna', 'sorna.integration'],

    python_requires='>=3.6',
    install_requires=[
        'sorna-client~=0.9.0',
        'metakernel>=0.20.1',
    ],
    extras_require={
        'dev': ['pytest', 'flake8'],
        'test': ['pytest'],
    },
    package_data={
    },
    data_files=[],
)
