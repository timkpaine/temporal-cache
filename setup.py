from setuptools import setup, find_packages
from codecs import open
import os
import os.path
import io

name = 'temporal-cache'
here = os.path.abspath(os.path.dirname(__file__))
pjoin = os.path.join


def get_version(file, name='__version__'):
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]

version = get_version(pjoin(here, 'temporalcache', '_version.py'))

with open(pjoin(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


requires = [
    'frozendict>=1.2',
    'tzlocal>=2.0.0',
]

requires_dev = [
    'flake8>=3.7.8',
    'mock',
    'pytest>=4.3.0',
    'pytest-cov>=2.6.1',
    'Sphinx>=1.8.4',
    'sphinx-markdown-builder>=0.5.2',
] + requires


setup(
    name=name,
    version=version,
    description='Time based function caching',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timkpaine/{name}'.format(name=name),
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='Apache 2.0',
    install_requires=requires,
    extras_require={
        'dev': requires_dev,
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='analytics tools',
    packages=find_packages(exclude=['tests', ]),
    include_package_data=True,
    zip_safe=False
)
