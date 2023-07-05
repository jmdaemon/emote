from setuptools import find_packages, setup
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    ''' Single source package version in src/package_name/__init__.py '''
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='sapply',
    version=get_version("src/sapply/__init__.py"),
    license='MIT',
    author='Joseph Diza',
    author_email='josephm.diza@gmail.com',
    description='Easily apply arbitrary string manipulations on text.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jmdaemon/sapply',
    project_urls={ 'Bug Tracker': 'https://github.com/jmdaemon/sapply/issues', },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={'': ['*.json']},
    python_requires='>=3.6',
    install_requires=['wora', 'spacy', 'regex', 'loguru'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sapply = sapply.main:main',
        ],
    },
    test_suite='test',
)
