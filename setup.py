from os import path
import setuptools


def get_requirements():
    """ Returns a list of required packages to be installed.
    Loads the list from the requirements.txt file. """

    this = path.realpath(__file__)
    here = path.dirname(this)
    requirements = path.join(here, 'requirements.txt')

    with open(requirements, 'r') as file:
        return file.read().splitlines()


setuptools.setup(
    name='reddit2instagram',
    version='0.0.1',
    author='Alon Krymgand Osovsky',
    author_email='downtown2u@gmail.com',
    description='Converting reddit submissions into instagram posts has never been easier.',
    url='https://github.com/reala10n/reddit2instagram',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    install_requirements=get_requirements(),
)
