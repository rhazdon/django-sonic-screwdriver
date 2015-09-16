import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sonic-screwdriver',
    version='21.1.19dev1',
    packages=find_packages(),
    license='MIT License',
    description='Django Sonic Screwdriver.',
    long_description='Django Sonic Screwdriver',
    url='https://github.com/rhazdon/django-sonic-screwdriver',
    author='Djordje Ilic',
    author_email='djordje.ilic@posteo.de',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
)
