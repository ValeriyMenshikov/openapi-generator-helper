from setuptools import setup, find_packages  # noqa: H301

NAME = "openapi_generator_helper"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    'requests'
]

setup(
    name=NAME,
    version=VERSION,
    description="openapi_generator_helper",
    author="Menshikov Valeriy",
    author_email="valeriy.menshikov.1989@gmail.com",
    url="https://github.com/ValeriyMenshikov/openapi-generator-helper.git",
    keywords=["OpenAPI", "OpenAPI-Generator", "openapi_generator_helper"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    package_data={'': ['python_templates/*.mustache',
                       'model_templates/*.mustache',
                       'tornado/*.mustache',
                       'asyncio/*.mustache']},
    long_description="""\
    Helper for dynamic generate and install python API client, generated by openapi-generator tool  # noqa: E501
    """
)
