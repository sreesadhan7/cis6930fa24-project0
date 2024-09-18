from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Sai Sree Sadhan Polimera',
	author_email='polimerasaisrees@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)