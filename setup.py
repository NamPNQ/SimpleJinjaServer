__author__ = 'nampnq'

from setuptools import setup

setup(
    name='SimpleJinjaServer',
    version='0.1',
    description="The tool help frontend developer for use jinja2 template",
    url="https://github.com/NamPNQ/SimpleJinjaServer",
    maintainer="nampnq",
    py_modules=['SimpleJinjaServer'],
    install_requires=[
        'flask'
    ]
)