import setuptools
import os
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


with open("README.md", "r") as fh:
    long_description = fh.read()

def compile_label_translations():
    import pathlib
    from pythongettext.msgfmt import Msgfmt
    curdir = pathlib.Path(__file__).parent.absolute()
    path_locales = os.path.join(curdir, 'browsesrt', 'locales')

    for (dirpath, dirnames, filenames) in os.walk(path_locales):
        po_file = next((x for x in filenames if is_po_file(x)), None)
        if po_file:
            name, extension = os.path.splitext(po_file)
            po_path = os.path.join(dirpath, po_file)
            mo_path = os.path.join(dirpath, name + '.mo')
            mo_bytes = Msgfmt(po_path).get()
            with open(mo_path, 'wb') as mo_file:
                mo_file.write(mo_bytes)

def is_po_file(filename):
    name, extension = os.path.splitext(filename)
    return extension == '.po'

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
