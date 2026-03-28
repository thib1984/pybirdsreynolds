# 🙏 Thanks !

Oh if you open this page, it's for contributing for this project, great ! A big thanks 🙏

To contribute, it's simple, check the [existing issues](https://github.com/thib1984/pybirdsreynolds/issues). If you see an issue you are interested to work, please let a message and i assign you the task. With this, all people know you are working on this issue.

If it's a new subject, don't hesitate to create an issue. I will check this one to affect some labels and let contribution open 😉

You can initialize a draft merge request directly when you start to work on an issue.

When you finish, past the merge request in "ready" mode and i will check this quickly.

If you are any questions, don't try to ping me 😁

# Work

```
# Uninstall the globally installed version via pipx if needed (optional, just to reset the published app)
pipx uninstall pybirdsreynolds 

# Clone the repository only the first time
git clone https://github.com/thib1984/pybirdsreynolds.git
# Afterwards, update it using regular git commands (git pull, git fetch, etc.)
cd pybirdsreynolds 

# Remove any previous virtual environment to start fresh
rm -rf pybirdsreynolds_env 

# Create a virtual environment to isolate dependencies for this project
python3 -m venv pybirdsreynolds_env
source pybirdsreynolds_env/bin/activate

# Install the local package in the isolated environment
pip install .

# Test the app locally within the virtual environment
pybirdsreynolds [...] 

# Optional: reinstall if needed and retest
pip install .
pybirdsreynolds [...] 

# Exit the virtual environment
deactivate

# Reinstall the globally published version via pipx if needed
pipx install pybirdsreynolds 
``` 

A venv (virtual environment) isolates this project's Python dependencies from the system, preventing version conflicts and keeping things clean.


# Publish to pypi

```
#from work directory
python3 -m build && python3 -m twine upload dist/* #to publish to pypi
```