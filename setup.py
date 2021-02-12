from setuptools import setup

setup(
    name="Portfolio Engineer",
    version="1.0",
    long_description=__doc__,
    packages=["Portfolio Engineer"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask"],
)