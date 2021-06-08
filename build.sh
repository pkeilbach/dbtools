rm -rf dist/ build/ dbtools.egg-info/
python setup.py sdist bdist_wheel
twine upload --repository-url http://pypiurlgoeshere dist/*