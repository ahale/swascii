from setuptools import setup

import swascii

setup(name='swascii',
      version=swascii.version,
      description='Swift Middlware',
      author='Andrew Hale',
      author_email='andy@wwwdata.eu',
      url='http://github.com/ahale/swascii/',
      packages=['swascii'],
      requires=['swift(>=1.7)', 'PIL(>=1.1.7)'],
      entry_points={'paste.filter_factory':
                    ['middleware=swascii.middleware:filter_factory']})
