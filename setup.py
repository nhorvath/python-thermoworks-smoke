from setuptools import setup, find_packages

setup(
    name='thermoworks_smoke',
    version='0.1.4',
    url='https://github.com/nhorvath/python-thermoworks-smoke',
    description='Pull data for your thermoworks smoke thermometer',
    author='nhorvath',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='Thermoworks',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyrebase4>=4.1.0'
    ]
)
