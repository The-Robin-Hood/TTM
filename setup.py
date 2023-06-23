from pathlib import Path
from setuptools import setup , find_packages
import os

def docs_read(fname):
    f = open(Path(__file__).parent.joinpath(fname)).read()
    return f.replace('â™¥', '♥')

def read_semver():
    return open(Path(__file__).parent.joinpath('src','pyttm','version.txt')).read().strip()

setup(
    name='pyttm',
    version=read_semver(),
    description='A simple Terminal based TOTP manager',
    long_description=(docs_read('README.md')),
    long_description_content_type='text/markdown',
    url='https://github.com/The-Robin-Hood/ttm',
    author='The Robin Hood',
    license='MIT',
    platforms=['any'],
    entry_points={
        'console_scripts': [
            'ttm = pyttm.app:main'
        ],
    },
    packages=find_packages(where='src',include=['pyttm','pyttm.*']),
    package_dir={'': 'src'},
    data_files=[("data", ["src/pyttm/version.txt"])],
    include_package_data=True,
    install_requires=['pycryptodome', 'requests'],
    keywords='totp,otp,encryption,decryption,AES256,crypto,security,privacy',
        classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Utilities',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3'
    ],
)