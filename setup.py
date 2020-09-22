from distutils.core import setup




setup(
  name = 'rancher_yarl',
  packages = ['rancher_yarl'],
  version = '0.2',
  description = 'Standalone rancher library, with API keys control',
  long_description="TEST",
    long_description_content_type='text/markdown',
author = 'gusto',                  
  author_email = 'shivering.fortune@gmail.com',      
  url = 'https://github.com/memdealer/YARL-YetAnotherRancherLibrary',  
  download_url = 'https://github.com/memdealer/YARL-YetAnotherRancherLibrary/archive/v0.1-alpha.tar.gz',   
  keywords = ['rancher', 'rancher api', 'rancher token'],   
  install_requires=[        
      'certifi',
      'chardet',
      'idna',
      'requests',
      'six',
      'urllib3',
      'websocket-client-py3'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
