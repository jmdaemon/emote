from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='sap-jmd',
    version='0.1.2',
    license='MIT',
    author='Joseph Diza',
    author_email='josephm.diza@gmail.com',
    description='Easily apply arbitrary string manipulations on text.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jmdaemon/sap',
    project_urls={ 'Bug Tracker': 'https://github.com/jmdaemon/sap/issues', },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    py_modules=['sap.charmap'],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sap = sap.cli:main',
        ],
    },
    test_suite='tests',
)
