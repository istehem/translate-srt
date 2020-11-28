import gettext

from os import path

from common.utils import projectroot
from browsesrt import browsesrt

def main():
    en = gettext.translation('browsesrt', localedir = path.join(projectroot(), 'browsesrt', 'locales'), languages=['en_US'])
    en.install()
    _ = en.gettext
    browsesrt.main()
