from setuptools import setup

setup(
    name="pybirds",
    version="0.1.0",
    description="pybirds game in terminam",
    long_description="The complete description/installation/use/FAQ is available at : https://github.com/thib1984/pybirds#readme",
    url="https://github.com/thib1984/pybirds",
    author="thib1984",
    author_email="thibault.garcon@gmail.com",
    license="MIT",
    packages=["pybirds"],
    install_requires=[],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pybirds=pybirds.__init__:pybirds"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
