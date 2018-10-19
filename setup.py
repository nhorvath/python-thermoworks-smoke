from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='thermoworks_smoke',
    version='0.1.7',
    url='https://github.com/nhorvath/python-thermoworks-smoke',
    description='Pull data for your thermoworks smoke thermometer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='nhorvath',
    author_email='nhorvath@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    keywords='Thermoworks',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyrebase4>=4.2.0'
    ]
)
