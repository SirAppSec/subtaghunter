from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="subtaghunter",
    version="0.1.0",
    author="SirAppSec",
    author_email="sirappsec@gmail.com",
    description="A tool to identify potential subdomain takeover vulnerabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sirappsec/subtaghunter",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "click",
        "yaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'subtaghunter=subtaghunter.core:main',
        ],
    },
    python_requires='>=3.6',
)
