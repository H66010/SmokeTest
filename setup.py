from setuptools import setup, find_packages

setup(
    name='Smoketest',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
        'allure-pytest',
        'pytest'
    ],
)
