from setuptools import setup, Extension,find_packages
from setuptools.command.build_ext import build_ext
import pybind11

ext_modules = [
    Extension(
        'pytca_cpp',
        ['pytca/cpp/pybind_module.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
    ),
]

setup(
    name='pytca',
    version='1.1.0',
    description='Advanced Python Library for Transaction Cost Analysis',
    author='Jialue Chen',
    author_email='jialuechen@outlook.com',
    url='https://github.com/jialuechen/pytca',
    packages=find_packages(),
    install_requires=[
        'pandas', 'matplotlib', 'plotly', 'bokeh', 'dash', 'flask', 'pybind11', 'numpy', 'geopandas', 'sklearn', 'textblob', 'requests', 'web3'
    ],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)

