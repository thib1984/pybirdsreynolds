from setuptools import setup

setup(
    name="pybirdsreynolds",
    version="1.99.18",
    description="pybirdsreynolds is a simulation of bird flocking behavior using Reynolds rules",
    long_description="This project is an interactive simulation of the Reynolds Boids model, implemented in Python with Tkinter. It allows you to visualize and experiment with the collective behavior of a flock of virtual birds by adjusting parameters such as cohesion, alignment, separation, speed, and neighborhood radius in real time. The interface also provides several controls (pause, reset, new generation, FPS display, etc.) to easily explore the dynamics of the system. The complete description/installation/use/FAQ is available at : https://github.com/thib1984/pybirdsreynolds#readme",
    url="https://github.com/thib1984/pybirdsreynolds",
    author="thib1984",
    author_email="thibault.garcon@gmail.com",
    license="MIT",
    license_files=[],
    packages=["pybirdsreynolds"],
    install_requires=[],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pybirdsreynolds=pybirdsreynolds.__init__:pybirdsreynolds"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",                
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)