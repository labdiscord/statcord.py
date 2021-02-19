from setuptools import setup

from statcord import __title__, __author__, __version__

if not __title__:
    raise RuntimeError("title is not set")
if not __author__:
    raise RuntimeError("author is not set")
if not __version__:
    raise RuntimeError("version is not set")

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=__title__,
    author=__author__,
    url="https://github.com/labdiscord/statcord.py/",
    version=__version__,
    packages=["statcord"],
    python_requires=">= 3.5",
    include_package_data=True,
    install_requires=requirements,
    description="A simple API wrapper for statcord.com to connect your bot and get your bot stats.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="statcord stat cord discordlabs discord labs bots statistics stats",
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
)
