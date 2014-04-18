import os
from distutils.core import setup
from setuptools import find_packages

install_requires = [
    'paramiko>=1.13.0',
    'pycurl>=7.19.0',
    'simplejson>=2.3.2',
    'tornado>=2.1',
    'scipy>=0.9.0',
    'rpy2>=1.03',
]


setup(
    name="HPC2",
    description="HPC2 Cloud execution",
    version=1.0,
    author="iMathResearch",
    author_email="info@imathresearch.com",
    url="www.imathresearch.com",
    package_dir={'HPC2': 'HPC2'},
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
