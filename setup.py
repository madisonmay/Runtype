from setuptools import setup, find_packages

setup(
    name="runtype",
    version="0.1.0",
    author="Madison May",
    author_email="madison@indico.io",
    packages=find_packages(
        exclude=[
            'tests'
        ]
    ),
    install_requires=[
        'decorator >= 4.0.10'
    ],
    description="""
        Runtime type checking made easy.
    """,
    license="MIT License (See LICENSE)",
    url="https://github.com/madisonmay/typed"
)
