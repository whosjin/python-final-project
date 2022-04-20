from setuptools import find_packages
from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name='Final Project',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/whosjin/python-final-project',
    author='Jin Hu',
    author_email='jzh0196@auburn.edu',
    description='Python (CPSC 4970) Final Project',
    long_description=long_description,
    install_requires={
        "PyQt5==5.15.6",
        "setuptools==62.1.0",
        "yagmail~=0.15.277",
        "pyqt5-tools=5.15.4",
        "keyring=23.5.0"
    },
    python_requires='>=3.9'
)
