from setuptools import setup, find_packages # Always prefer setuptools over distutils

setup(
    name = 'translatesrt',

    version = '0.0.1',

    description='Translate sub-title files',

    author = 'Oskar Ingemarsson',

    author_email = 'oskar.ingemarsson@gmail.com',

    license = 'BSD3',

    packages = find_packages(exclude=[]),

    keywords = 'MPD REST JSON',

    classifiers = ['Programming Language :: Python :: 3'],
)
