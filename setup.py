import ast
import re
import sys

from setuptools import find_packages, setup


def is_psycopg2_exists():
    try:
        import psycopg2
        return True
    except ImportError:
        return False


def get_install_requires():
    install_requires = [
        "PyQt5",
        "qdarkstyle",
        "requests",
        "websocket-client",
        "peewee",
        "pymysql",
        "mongoengine",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "tigeropen",
        "rqdatac",
        "ta-lib",
        "ibapi",
        "deap"
    ]
    if not is_psycopg2_exists():
        install_requires.append("psycopg2-binary")

    if sys.version_info.minor < 7:
        install_requires.append("dataclasses")
    return install_requires


def get_version_string():
    global version
    with open("vnpy/__init__.py", "rb") as f:
        version_line = re.search(
            r"__version__\s+=\s+(.*)", f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


setup(
    name="pyalgotrader",
    version=get_version_string(),
    author="Alex Hurko (forked and modified original repository https://github.com/vnpy/vnpy)",
    author_email="alex1hurko@gmail.com",
    license="MIT",
    url="",
    description="Python algorithmic trading framework",
    long_description=__doc__,
    keywords='quant quantitative investment trading algotrading',
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"": [
        "*.ico",
        "*.ini",
        "*.dll",
        "*.so",
        "*.pyd",
    ]},
    install_requires=get_install_requires(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows Server 2008",
        "Operating System :: Microsoft :: Windows :: Windows Server 2012",
        "Operating System :: Microsoft :: Windows :: Windows Server 2012",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],

)
