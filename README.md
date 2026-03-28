# pybirdsreynolds

This project is an interactive simulation of the Reynolds Boids model, implemented in Python with Tkinter. It allows you to visualize and experiment with the collective behavior of a flock of virtual birds by adjusting parameters such as cohesion, alignment, separation, speed, and neighborhood radius in real time. The interface also provides several controls (pause, reset, new generation, FPS display, etc.) to easily explore the dynamics of the system.

<img width="1451" height="666" alt="image" src="https://github.com/user-attachments/assets/a5a50a62-989c-457c-a0c4-a86240210f7b" />

# Installation/Upgrade/Use

## Prerequisites

- Install Python 3 on your system
- Install pipx on your system
- Install git on your system

## Why use pipx?

`pipx` installs Python applications in isolated environments, which prevents dependency conflicts with your system or other projects.  
It also allows you to run CLI tools globally without polluting your Python installation.  
This makes it safer and cleaner than using `pip` or `pip3` for installing standalone tools.

## Clean old versions

If you have installed an old version with `pip` or `pip3` (depending on your system), use one of the following commands:

```
pip3 uninstall pybirdsreynolds
pip uninstall pybirdsreynolds
pip3 uninstall pybirdsreynolds --break-system-packages
pip uninstall pybirdsreynolds --break-system-packages
```

## Installation

```
pipx install pybirdsreynolds
```

## Upgrade

```
pipx upgrade pybirdsreynolds --include-deps
```

This command upgrades the application to the latest version and also updates all its dependencies.

## Uninstall

```
pipx uninstall pybirdsreynolds
```

## Use

```pybirdsreynolds```

- If you obtain error about tk, install python3-tk
``` 
sudo apt install python3-tk #for ubuntu
sudo pacman -S tk #for arch
brew install python-tk #for mac
```

## Documentation and options

```pybirdsreynolds --help```
