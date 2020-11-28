import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


with open("README.md", "r") as fh:
    long_description = fh.read()

def compile_label_translations():
    import os
    import sys
    import pathlib
    from pythongettext.msgfmt import Msgfmt
    curdir = pathlib.Path(__file__).parent.absolute()
    path = os.path.join(curdir, 'browsesrt', 'locales', 'en_US', 'LC_MESSAGES')
    po_path = os.path.join(path, 'browsesrt.po')
    mo_bytes = Msgfmt(po_path).get()
    mo_path = os.path.join(path, 'browsesrt.mo')
    with open(mo_path, 'wb') as mo_file:
        mo_file.write(mo_bytes)


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        compile_label_translations()


class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)
        compile_label_translations()

setuptools.setup(
    name = 'translate-srt',

    version = '0.0.1',

    description='Translate sub-title files',

    long_description=long_description,

    author = 'Oskar Ingemarsson',

    author_email = 'oskar.ingemarsson@gmail.com',

    license = 'BSD3',

    packages = setuptools.find_packages(),

    keywords = 'Translate, Subtitles',

    classifiers = ['Programming Language :: Python :: 3'],

    install_requires=['ZODB', 'requests', 'urwid', 'python-gettext'],

    entry_points = {
        'console_scripts' : [
            'translate-srt = translatesrt:main',
            'delay-srt = delaysrt:main',
            'browse-srt = browsesrt:main'
            ]
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': egg_info
    }
)
