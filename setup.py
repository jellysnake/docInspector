from setuptools import setup, find_packages

setup(
    name='DocInspector',
    version='0.1.0',
    author='Quinn Roberts, Simon Schippl, Darcy Trenfield & Ganesh Ukwatt',
    url='https://git.infotech.monash.edu/FIT2101-S2-2018-Scrumbags',
    author_email="invalid@invalid.com",
    license='LICENSE.txt',
    description='A program made to provide statistical information about google documents and their revisions',
    long_description=open('README.md').read(),
    install_requires=[
        "oauth2client >= 4.1",
        "google-api-python-client >=1.7",
        'httplib2'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'DocInspector=DocInspector.docInspector:main'
        ]
    },
    include_package_data=True

)
