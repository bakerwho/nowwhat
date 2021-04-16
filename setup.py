from glob import glob
import os
import sys
from setuptools import setup

if sys.version_info[:2] < (3, 5):
    error = (
        "NOWwhat requires Python 3.5 or later (%d.%d detected). \n"
    )
    sys.stderr.write(error + "\n")
    sys.exit(1)


name = "nowwhat"
version = '0.1'
description = "Python package for working with NOW corpus data"
authors = {
    "Abubaker-Kar": ("Aabir Abubaker-Kar", "aabir.abubaker.kar@gmail.com")
}
maintainer = "Aabir Abubaker Kar"
maintainer_email = "aabir.abubaker.kar@gmail.com"

platforms = ["Linux", "Mac OSX", "Windows", "Unix"]

def parse_requirements_file(filename):
    with open(filename) as fid:
        requires = [l.strip() for l in fid.readlines() if not l.startswith("#")]

    return requires

install_requires = parse_requirements_file("requirements.txt")

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":

    setup(
        name=name,
        version=version,
        maintainer=maintainer,
        maintainer_email=maintainer_email,
        author=authors["Abubaker-Kar"][0],
        author_email=authors["Abubaker-Kar"][1],
        description=description,
        #keywords=keywords,
        long_description=long_description,
        platforms=platforms,
        install_requires=install_requires,
        python_requires=">=3.5",
        zip_safe=False,
    )
