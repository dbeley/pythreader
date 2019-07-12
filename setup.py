import setuptools
import pythreader

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythreader",
    version=pythreader.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="pythreader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/pythreader",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["pythreader=pythreader.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["tweepy", "numpy", "pillow", "urllib3"],
)
