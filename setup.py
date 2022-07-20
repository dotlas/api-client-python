from setuptools import setup, find_packages

setup(
    name="dotlas",
    version="1.0.2",
    description="Dotlas Python Package",
    author="Dotlas Inc.",
    author_email="tech@dotlas.com",
    url="https://github.com/dotlas/api-client-python",
    packages=find_packages(),
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pydantic",
        "requests"
    ]
)
