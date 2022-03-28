from setuptools import setup, find_packages

setup(
    name="dotlas",
    version="1.0",
    description="Dotlas Python Package",
    url="https://github.com/dotlas/api-client-python",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic",
        "requests"
    ]
)
