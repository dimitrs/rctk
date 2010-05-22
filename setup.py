from setuptools import setup, find_packages
import sys, os

version = '0.1'

if sys.version_info[0] == 3: # python 3
    install_requires = []
    entry_points={
        "console_scripts": [
          "serve_py3=rctk.serve_py3:main",
    ]}
else:
    install_requires=[
          'py',
          'web.py',
          'simplejson'
    ]
    entry_points={
        "console_scripts": [
          "test=rctk.runtests:runall",
          "serve_webpy=rctk.serve_webpy:main",
          "serve_mozilla=rctk.serve_mozilla:main",
          "serve_process=rctk.serve_process:main"
    ]}
    
setup(name='rctk',
      version=version,
      description="RemoteControl Toolkit",
      long_description="""\
A Dektop widget library that uses a browser to render widgets""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ivo van der Wijk',
      author_email='ivo@m3r.nl',
      url='http://rctk.googlecode.com',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points=entry_points,
      )
