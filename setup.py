from setuptools import setup

setup(
    name="gallery-dl-wrapper",
    version="1.0.2",
    install_requires=['beautifulsoup4', 'gallery-dl', 'requests'],
    entry_points={
        "console_scripts": [
            "gdw = main:main",
        ],
    }
)
