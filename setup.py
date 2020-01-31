import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="processit-pkg", # Replace with your own username
    version="0.0.1",
    author="marvin",
    author_email="marvin.casagnap@gmail.com",
    description="A small project using python3 in processing files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marzim/processit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)