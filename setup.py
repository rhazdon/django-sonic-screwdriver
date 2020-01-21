import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-sonic-screwdriver",
    version="0.2.3",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="Django Sonic Screwdriver is a collection of very useful commands and will make your life easier.",
    long_description=README,
    url="https://github.com/rhazdon/django-sonic-screwdriver",
    author="Djordje Atlialp",
    author_email="djordje@atlialp.com",
    install_requires=["django", "djangorestframework", "wheel"],
    tests_require=["coverage", "django", "djangorestframework", "coveralls"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
)
