from setuptools import setup, find_namespace_packages
from pathlib import Path


setup(
    name='backend.ai-integration-jupyter',
    version='0.3.1',
    description='Backend.AI Integration for Jupyter',
    long_description=Path('README.md').read_text() + Path('CHANGELOG.md').read_text(),
    long_description_content_type='text/markdown',
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
    project_urls={
        'Documentation': 'http://docs.backend.ai',
        'Source': 'https://github.com/lablup/backend.ai-integration-jupyter',
        'Tracker': 'https://github.com/lablup/backend.ai-integration-jupyter/issues',
    },

    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src', include='ai.backend.*'),

    python_requires='>=3.5',
    install_requires=[
        'backend.ai-client>=1.4.0,<1.5.0',
        'metakernel~=0.20.14',
    ],
    extras_require={
        'build': ['wheel>=0.31.0', 'twine>=0.11.0'],
        'dev': ['pytest', 'flake8'],
        'test': ['pytest'],
    },
    setup_requires=[
        'setuptools>=40.1.0',
    ],
    package_data={
    },
    data_files=[],
)
