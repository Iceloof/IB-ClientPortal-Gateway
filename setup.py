import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ib-cp-gateway",
    version="1.0.1",
    author="Hurin Hu",
    author_email="hurin@live.ca",
    description="This is a simple IB Client Portal Gateway RESTFul api, IB Client Portal Gateway can be run on Raspberry Pi or any other ARM machine(IB Gateway and TWS are not able to run on ARM).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iceloof/IB-ClientPortal-Gateway",
    packages=setuptools.find_packages(),
    install_requires=['urllib3','requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
