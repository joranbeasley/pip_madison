import setuptools
import pip_madison
setuptools.setup(
    name="pip-madison",
    version=pip_madison.__version__,
    author="Joran Beasley",
    author_email="joranbeasley@gmail.com",
    description="A simple tool to list available version releases",
    packages=['pip_madison'],
    entry_points={
        'console_scripts':['pip-madison=pip_madison.cli:list_versions'],
    },
    install_requires=['click','bs4','requests','six','pySystem'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)