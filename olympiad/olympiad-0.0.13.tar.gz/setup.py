from setuptools import setup, find_packages

setup(name='olympiad',
      version='0.0.13',
      packages=[package for package in find_packages()
                if package.startswith('gym_vnc')],
      install_requires=['gym>=0.5.2' 'Pillow', 'autobahn',
                        'twisted', 'ujson', 'six', 'PyYAML',
                        'fastzbarlight>=0.0.13',
                        # Not actually needed, but Twisted will print
                        # scary warnings unless it's installed
                        #
                        # Don't install yet since it has some annoying dependencies (libffi)
                        #
                        # 'service_identity'
      ],
      extras_require={
          'atari': 'gym[atari]',
          # Faster vnc driver
          'production': ['go-vncdriver>=0.4.0'],
          # 'libvnc': ['libvncdriver'],
          'docker': ['docker-py'],
      }
)
