from setuptools import setup, find_packages

setup(
    name="academic_paper_analyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
        "tqdm",
        "pandas",
        "pydantic",
        "langchain",
        "langchain-openai",
        "langchain-community",
        "pymupdf"
    ],
)