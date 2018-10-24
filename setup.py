#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uloganalysis",
    version="0.0.4",
    author="Dennis Mannhart",
    author_email="dennis.mannhart@gmail.com",
    description="A package to analys ulog files using pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YUNEEC/ulogAnalysis",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'pyulog',
        'transforms3d'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
