from distutils.core import setup
setup(
  name = 'rancher-yarl',
  packages = ['rancher-yarl'],
  version = '0.1',
  license='GPL3',
  description = 'Standalone rancher library, with API keys control',
  author = 'gusto',                  
  author_email = 'uncupoftea@gmail.com',      
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
    'License :: OSI Approved :: GPL3 licensee', 
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
