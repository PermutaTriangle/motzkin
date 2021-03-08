#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="motzkin",
    version="0.0.1",
    author="Christian Bean",
    author_email="christianbean@ru.is",
    description="A library for counting and sampling sets of Motzkin paths avoiding patterns.",
    license="BSD-3",
    keywords="enumerative combinatorics combinatorial specification counting motzkin paths sampling random",
    url="https://github.com/PermutaTriangle/motzkin",
    project_urls={
        "Source": "https://github.com/PermutaTriangle/motzkin",
        "Tracker": ("https://github.com/PermutaTriangle/motzkin" "/issues"),
    },
    packages=find_packages(),
    package_data={"motzkin": ["py.typed"]},
    long_description=read("README.md"),
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    install_requires=[
        "comb_spec_searcher==3.0.0",
    ],
)
