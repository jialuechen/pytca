from setuptools import setup, find_packages

from pytca import __version__ as version

full_description = """pytca is a Python library for doing transaction cost analysis (TCA), essentially finding the cost of your trading activity.
Across the industry many financial firms and corporates trading within financial markets spend a lot of money on TCA, either
by developing in house tools or using external services.Many sell side firms and larger buy side firms build and maintain their own TCA libraries, which is very expensive. The cost of TCA
across the industry is likely to run into many hundreds of millions of dollars or possibly billions of dollars.

Much of the complexity in TCA is due to the need to handle large tick datasets and do calculations on them and is largely a
software engineering problem. This work needs to be repeated in every single implementation. By open sourcing the library
we hope that the industry will no longer need to keep reinventing the wheel when it comes to TCA. At the same time,
because all the code is visible to users, pytca allows you can add your own customized metrics and benchmarks,
which is where you are likely have very particular IP in financial markets. You get the flexibility of a fully internal
TCA solution for free.
"""

with open('requirements.txt') as f:
    install_requires = f.read()

setup(name='pytca',
      version=version,
      description='Tranasction cost analysis library',
      author='Jialue Chen',
      author_email='jialuechen@outlook.com',
      license='BSD',
      long_description=full_description,
      keywords=['TCA', 'transaction cost analysis'],
      url='https://github.com/jialuechen/pytca',
      packages=find_packages(include=["pytca*"]),
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)
