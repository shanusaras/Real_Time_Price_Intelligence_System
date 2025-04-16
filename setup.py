from setuptools import setup, find_packages

setup(
    name="price_intelligence",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "mysqlclient",
        "pymongo",
        "pandas",
        "python-dotenv",
        "sqlalchemy-utils",
    ],
)
