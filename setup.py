#!/usr/bin/env python


from pathlib import Path
try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")


readme = Path("README.md")
license = Path("LICENSE")


# Read the version without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = "0.7"

NAME = 'somedecorators'
VERSION = version
DESCRIPTION = 'Some useful decorators in Python.'
KEYWORDS = 'awesome decorators'
AUTHOR = 'somenzz'
AUTHOR_EMAIL = 'somenzz@163.com'
URL = 'https://github.com/somenzz/somedecorators'
LICENSE = license.read_text()
PACKAGES = find_packages(exclude=['tests', 'tests.*'])

INSTALL_REQUIRES = ['djangomail']
TEST_SUITE = 'tests'
TESTS_REQUIRE = []

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

LONG_DESCRIPTION = readme


params = {
    'name':             NAME,
    'version':          VERSION,
    'description':      DESCRIPTION,
    'keywords':         KEYWORDS,
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'url':              URL,
    'license':          "MIT",
    'packages':         PACKAGES,
    'install_requires': INSTALL_REQUIRES,
    'tests_require':    TESTS_REQUIRE,
    'test_suite':       TEST_SUITE,
    'classifiers':      CLASSIFIERS,
    'long_description': readme.read_text()
}

if __name__ == '__main__':
    setup(**params,long_description_content_type='text/markdown')
