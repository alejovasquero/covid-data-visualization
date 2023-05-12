from distutils.core import setup

from setuptools import find_packages

setup(
    name='CovidData',
    version='0.1dev',
    packages=find_packages('src'),
    long_description=open('README.txt').read(),
)