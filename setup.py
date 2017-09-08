import json
import os

from setuptools import setup, find_packages


def _readfile(filename):
    with open(filename, encoding='utf-8') as fp:
        contents = fp.read()
    return contents


def _get_packages(path):
    out = [path]
    for x in find_packages(path):
        out.append('{}/{}'.format(path, x))
    
    return out


def _get_extra_packages():
    with open(os.path.join(os.path.dirname(__file__), "extra_requirements.json")) as f:
        return json.load(f)


def _get_requirements():
    return _readfile(os.path.join(os.path.dirname(__file__), "requirements.txt"))

setup(name='event_mill',
      version='0.1.0',
      description='A framework for projections from event stores',
      url='https://github.com/fcracker79/event_mill',
      #      author='',
      #      author_email='',
      license='MIT',
      packages=_get_packages('event_mill'),
      install_requires=_get_requirements(),
      extras_require=_get_extra_packages(),
      zip_safe=False,
      test_suite="test",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='event DDD domain projection store'
      )
