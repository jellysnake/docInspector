from setuptools import setup, find_packages

setup(
    name='DocInspector',
    version='0.1.0',
    author='Quinn A. R. Roberts',
    url='https://github.com/jellysnake/docInspector',
    author_email="iamajellysnake@gmail.com",
    license='LICENSE.txt',
    description='A program made to provide statistical information about google documents and their revisions',
    long_description=open('README.md').read(),
    install_requires=[
        "oauth2client == 4.1",
        "google-api-python-client ==1.7",
        'httplib2', 'yattag'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'DocInspector=DocInspector.docInspector:main'
        ]
    },
    include_package_data=True

)
