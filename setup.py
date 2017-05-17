from distutils.core import setup

setup(
      name='dork-enum',
      version='0.1',
      author='Steve Coward',
      author_email='steve.coward@gmail.com',
      url='https://github.com/stevecoward/dork-enum',
      scripts=['bin/dorkenum'],
      license='LICENSE',
      description='Tool that accepts a GoogleDork string and performs a set of actions.',
      packages=['dorkenum','dorkenum.helpers'],
      install_requires=[
      	'beautifulsoup4',
      	'click',
      	'geoip2',
      	'requests',
      	'tldextract',
      ]
)
