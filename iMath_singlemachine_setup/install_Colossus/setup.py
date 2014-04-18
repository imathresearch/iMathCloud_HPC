import os
from distutils.core import setup
from setuptools import find_packages

install_requires = [
    'paramiko>=1.13.0',
    'numpy>=1.6.1',
    'psycopg2>=2.4.5',
    'pyMongo>=2.1',
    'tornado>=2.1',
    'scipy>=0.9.0',
    'scikit-learn>=0.10',
    'rpy2>=1.03',
]


setup(
    name="Colossus",
    description="Colossus development framework",
    version=1.0,
    author="iMathResearch",
    author_email="info@imathresearch.com",
    url="www.imathresearch.com",
    package_dir={'Colossus': 'Colossus'},
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
