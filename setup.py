from setuptools import setup
from pathlib import Path


setup(
    name='backend.ai-integration-jupyter',
    version='0.2.0',
    description='Backend.AI Integration for Jupyter',
    long_description=Path('README.rst').read_text(),
    url='https://github.com/lablup/backend.ai-integration-jupyter',
    author='Lablup Inc.',
    author_email='joongi@lablup.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],

    packages=[
        'ai.backend.integration.jupyter',
    ],

    python_requires='>=3.5',
    install_requires=[
        'backend.ai-client~=1.0.0',
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
