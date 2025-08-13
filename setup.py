from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in fleet_system/__init__.py
from fleet_system import __version__ as version

setup(
	name="fleet_system",
	version=version,
	description="Fleet management systems",
	author="Ubaid Ali",
	author_email="ubaidkhanzada8@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
