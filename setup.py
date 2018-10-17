from setuptools import setup, find_packages

setup(
    name="DocInspector",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docInspector=docInspector:main'
        ]
    }
)
