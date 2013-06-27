try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(packages=['blackmamba'],
        requires=['adns'],
        name='blackmamba',
        long_description=open('Readme.md').read(),
        )
