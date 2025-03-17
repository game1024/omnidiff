from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r") as f:
  long_description = f.read()

setup(name='omnidiff',
      version='1.3',
      description='A diff toolkit for python',
      author='game1024',
      author_email='pengbin.xyz@gmail.com',
      url='https://github.com/game1024/omnidiff',
      install_requires=["jmespath"],
      license='MIT',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
      ],
      python_requires='>=3',
      )
