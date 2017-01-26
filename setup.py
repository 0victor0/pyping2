#!/usr/bin/env python

from setuptools import setup, find_packages

author          = "Victor Clark"
appname         = "pyping2"
kwords          = "network analysis reporting docker reverse engineering"
requirements    = ["pandas"]

try:
    import pyping2
    version = pyping2.__version__
except:
    version = None

if __name__ == '__main__':
    setup(
        name                = appname,
        keywords            = kwords,
        version             = version,
        description         = 'Network analysis and reporting library',
        author              = 'Victor Clark',
        url                 = "https://www.github.com/0victor0/pyping2",
        license             = "https://www.gnu.org/licenses/gpl-3.0.html",
        install_requires    = requirements,
        packages            = find_packages(),
        zip_safe            =True
    )