from setuptools import setup, find_packages

setup(
    name="cwtlib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "requests",
        "cwt-units-converter",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for water treatment calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cwtlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
