import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_order_utils",
    version="0.3.2",
    author="Kuest Engineering",
    author_email="support@kuest.com",
    maintainer="Kuest Engineering",
    maintainer_email="support@kuest.com",
    description="Python utilities used to generate and sign orders for the Kuest CTF Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuestcom/python-order-utils",
    install_requires=[
        "eth-utils>=4.1.1",
        "eth-account>=0.13.0",
        "poly-eip712-structs",
        "pytest",
    ],
    package_data={
        "py_order_utils": [
            "abi/*.json",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/kuestcom/python-order-utils",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9.10",
)
