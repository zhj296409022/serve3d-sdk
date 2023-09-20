from setuptools import setup, find_packages 
from pkg_resources import parse_requirements 

with open('requirements.txt', encoding='utf-8') as fp: 
  install_requires = [str(requirement) for requirement in parse_requirements(fp)] 

__author__ = 'Shendi Tech' 
__version__ = '0.1.0' 

setup( 
  name='serve3d sdk', 
  version=__version__, 
  author=__author__, 
  author_email='296409022@qq.com', 
  description='serve3d sdk', 
  packages=find_packages(where='serve3d_sdk'), 
  install_requires=install_requires 
) 

