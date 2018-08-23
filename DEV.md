Developing
==========

Create a new virtualenv and install the required libraries

```
mkvirtualenv -p python3 python-thermoworks-smoke # if you have virtualenvwrapper installed
pip install --upgrade -r requirements.txt
```

Building
========

1. Install/Update build dependencies:
`pip install --upgrade -r requirements.build.txt`
1. Increment the version number in setup.py
1. Create the package files:
`python setup.py sdist bdist_wheel`
1. Upload to test pypi repo:
`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
1. Check that package installs and works in another project:
`pip install --index-url https://test.pypi.org/simple/ thermoworks-smoke==[new version]`
1. Upload to main pypi repo:
`twine upload dist/*`

NOTE: Registration for https://test.pypi.org is separate from https://pypi.org