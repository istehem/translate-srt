import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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

    install_requires=['ZODB', 'requests', 'flask', 'Flask-RESTful'],

    entry_points = {
        'console_scripts' : ['translate-srt = translatesrt:main', 'delay-srt = delaysrt:main', 'srt-web-tools = srtwebtools:main']
    }

)
