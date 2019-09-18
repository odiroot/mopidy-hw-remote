#!/usr/bin/env python
import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8'),
    ) as fh:
        return fh.read()


setup(
    name='mopidy-rpi-remote',
    version='0.1.0',
    license='Apache',
    description='Remote controller for Mopidy running on Raspberry Pi Zero W',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Michal Odnous',
    author_email='odiroot@users.noreply.github.com',
    url='https://github.com/odiroot/mopidy-hw-remote',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia',
        'Topic :: Utilities',
    ],
    python_requires='>=3.5',
    install_requires=[
        'luma.oled~=3.3.0',
        'paho-mqtt~=1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'mopidy_remote = mopidy_rpi_remote.cli:main'
        ]
    },
)
