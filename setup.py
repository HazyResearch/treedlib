from setuptools import setup, find_packages

setup(
    name='treedlib',
    version='0.1.1',
    description='Library of tree features.',
    packages=find_packages(),
    install_requires=[
        'lxml',
    ],
    url='https://github.com/HazyResearch/treedlib',
    author='Hazy Research',
)
