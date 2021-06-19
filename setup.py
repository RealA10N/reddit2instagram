from os import path, listdir
import re
import setuptools

from reddit2instagram import __version__

THIS = path.realpath(__file__)
HERE = path.dirname(THIS)


def get_requirements(filename: str):
    """ Returns a list of required packages to be installed.
    Loads the list from the requirements.txt file. """

    with open(path.join(HERE, filename), 'r') as file:
        return file.read().splitlines()


def get_extra_requirements():
    """ Loads all local files with the following filename format:
    `requirements-%s.txt`. Returns a dict of extra requirements. """

    # Get a list of all extra requirements filenames
    extra_files = [
        filename
        for filename in listdir(HERE)
        if all((
            path.isfile(path.join(HERE, filename)),
            re.match('^requirements-[a-z]+.txt$', filename)
        ))
    ]

    get_extra_name = lambda filename: re.search(
        r'-.*\.', filename).group()[1:-1]

    # For each file, load data and return it
    return {
        get_extra_name(filename): get_requirements(filename)
        for filename in extra_files
    }


setuptools.setup(
    name='reddit2instagram',
    version=__version__,
    author='Alon Krymgand Osovsky',
    author_email='downtown2u@gmail.com',
    description='Converting reddit submissions into instagram posts has never been easier.',
    url='https://github.com/reala10n/reddit2instagram',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    install_requires=get_requirements('requirements.txt'),
    extras_require=get_extra_requirements(),
)
