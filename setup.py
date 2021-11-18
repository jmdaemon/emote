import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sap-jmd",
    version="0.0.1",
    author="Joseph Diza",
    author_email="josephm.diza@gmail.com",
    description="Apply a series of string manipulations on text easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmdaemon/sap",
    project_urls={
        "Bug Tracker": "https://github.com/jmdaemon/sap/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    py_modules=['sap'],
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'sap = sap:main',
        ],
    },

)