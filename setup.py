from setuptools import setup , find_packages
import os

def docs_read(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname)).read()
    return f.replace('â™¥', '♥')

setup(
    name='pyttm',
    version='0.0.3',
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
    include_package_data=True,
    install_requires=['pycryptodome'],
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