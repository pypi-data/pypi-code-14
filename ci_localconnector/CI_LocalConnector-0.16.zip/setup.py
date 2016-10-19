from distutils.core import setup
setup(name='CI_LocalConnector',
      version='0.16',
      py_modules=['CI_LocalConnector' , 'CI_LC_BL'],
	  description="IOT application that collect data from PLC (ModBus or AnB Ethernet/IP) and send to cloud using https",
	  author="Ido Peles",
	  author_email="idop@contel.co.il",
          install_requires=['pymodbus'],
      )
