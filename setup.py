import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


with open("README.md", "r") as fh:
    long_description = fh.read()

def custom_command():
    import os
    import sys
    import pathlib
    import subprocess
    curdir = pathlib.Path(__file__).parent.absolute()
    os.chdir(os.path.join(curdir, 'browsesrt', 'locales', 'en_US', 'LC_MESSAGES'))
    subprocess.check_output(['msgfmt', '-o', 'browsesrt.mo', 'browsesrt'])
    os.chdir(curdir)


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        custom_command()


class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)
        custom_command()


class CustomEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command()

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

    install_requires=['ZODB', 'requests', 'urwid', 'django'],

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
        'egg_info': CustomEggInfoCommand,
    }
)
