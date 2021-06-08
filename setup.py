import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='dbtools',
    version='1.4.0',
    author='PK17',
    author_email='python@pk17.org',
    description='A convenience wrapper for MySQL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    install_requires=[
        'mysql-connector-python',
        'pandas'
    ],
    dependency_links=[
        '',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: TODO',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
