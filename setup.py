from setuptools import setup, Extension,find_packages
from setuptools.command.build_ext import build_ext


setup(
    name='pytca',
    version='1.1.0',
    description='Python Library for Transaction Cost Analysis',
    author='Jialue Chen',
    author_email='jialuechen@outlook.com',
    url='https://github.com/jialuechen/pytca',
    packages=find_packages(),
    install_requires=[
        'pandas', 'matplotlib', 'plotly', 'bokeh', 'dash', 'flask', 'pybind11', 'numpy', 'geopandas', 'sklearn', 'textblob', 'requests', 'web3'
    ],
    cmdclass={'build_ext': build_ext},
)

