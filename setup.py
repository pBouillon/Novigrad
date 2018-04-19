from codecs import open
from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='novigrad',

    version='1.0.0',

    description='Novigrad is a small tool built to check your dependencies',
    long_description=long_description,

    url="http://github.com/pBouillon/Novigrad",

    author="Pierre Bouillon, Florian Vaissiere",
    author_email='pierre.bouillon@openmailbox.org',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='dependency git github',

    packages=find_packages(),
)
