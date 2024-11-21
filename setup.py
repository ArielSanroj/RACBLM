import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from setuptools import setup, find_packages

setup(
    name="my_project",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "streamlit>=1.40.1",
        "openai",
        "python-dotenv",
        "sqlalchemy",
    ],
)