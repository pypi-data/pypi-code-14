def getCDFs(date, craft, species='H', RBlevel='3PAP', Hlevel='3', Hproduct='PA', Maglevel='3', EMlevel='3', PH='LEHT', EMF='1sec-sm',
            check=True, all=True, TOFxE=False, TOFxPH=False, HOPE=False, MagEIS=False, EMFISIS=False):
    '''
    getCDFs(getCDFs(datetime, string, string, **kw):

    date: Python datetime object containing the date that you want cdfs for.
    craft: character - 'A' or 'B'.
    species: character - 'H', 'He', or 'O'.
    RBlevel: string - RBSPICE data level; '3PAP', '3', '2', '1', or '0'
    Hlevel: string - HOPE data level; '3', or '2'
    Hproduct: string - If using, HOPE level 3 data, which product; 'PA' or 'MOM'
    Maglevel: string - MagEIS data level; '3', or '2'
    EMlevel: string - EMFISIS data level; '4', '3', or '2'
    PH: string describing which Time of Flight by Pulse Height product you want: 'LEHT'(Low Energy, High Time resolution) or 'HELT'(High Energy, Low Time resolution).
    EMF: string describing which EMFISIS product you want: ('1sec', '4sec', or 'hires')+'-'+('gei', 'geo', 'gse', 'gsm', or 'sm').
    check: When True, it will query the server for updated versions, if it is False, then the server will not be queried at all. If you don't have the file on your computer, it will not be downloaded. Set this keyword to False if you do not have internet access.
    The last five keywords describe which data product you want, all is default, but if you set any one or more of them to True, then you will only get what you set to True.

    Returns: Python dictionary containing spacepy cdf objects. Keys are 'TOFxE', 'TOFxPH', 'HOPE', and 'EMFISIS'
    '''
    
    import sys
    import requests
    from os.path import isfile, join, normpath
    from os import remove, listdir, stat, makedirs, getenv
    from fnmatch import filter
    from bs4 import BeautifulSoup
    from urllib.request import urlretrieve
    import spacepy.pycdf as cdf
    from configparser import ConfigParser
    from datetime import datetime
    
    if not (type(date) is datetime):
        raise ValueError('Invalid date format, use datetime')
        
    if not (type(craft) is str):
        raise ValueError('Invalid craft input, use string')
    else:
        craft = craft.upper()
        
    if not craft in ['A', 'B']:
        raise ValueError('Invalid craft input, \'A\' or \'B\'')
        
    if not (type(species) is str):
        raise ValueError('Invalid species input, use string')
    else:
        species = species.capitalize()
        
    if not species in ['H', 'He', 'O']:
        raise ValueError('Invalid species input, \'H\', \'He\', or \'O\'')
        
    if not (type(RBlevel) is str):
        raise ValueError('Invalid RBlevel input, use string')
    else:
        RBlevel = RBlevel.upper()
        
    if not RBlevel in ['3PAP', '3', '2', '1', '0']:
        raise ValueError('Invalid RBlevel input, \'3PAP\', \'3\', \'2\', \'1\', or \'0\'')
        
    if not Hlevel in ['3', '2']:
        raise ValueError('Invalid Hlevel input, \'3\', or \'2\'')
        
    if not (type(Hproduct) is str):
        raise ValueError('Invalid Hproduct input, use string')
    else:
        Hproduct = Hproduct.upper()
        
    if not Hproduct in ['PA', 'MOM']:
        raise ValueError('Invalid Hproduct input, \'PA\', or \'MOM\'')
        
    if not Maglevel in ['3', '2']:
        raise ValueError('Invalid Maglevel input, \'3\', or \'2\'')
        
    if not EMlevel in ['4', '3', '2']:
        raise ValueError('Invalid RBlevel input, \'4\', \'3\', or \'2\'')
        
    if not (type(PH) is str):
        raise ValueError('Invalid PH input, use string')
    else:
        PH = PH.upper()
        
    if not PH in ['LEHT', 'HELT']:
        raise ValueError('Invalid RBlevel input, \'LEHT\', or \'HELT\'')
        
    if not (type(EMF) is str):
        raise ValueError('Invalid EMF input, use string')
    else:
        EMF = EMF.lower()
        
    if not EMF in [a+'-'+b for a in ['1sec', '4sec', 'hires'] for b in ['gei', 'geo', 'gse', 'gsm', 'sm']]:
        raise ValueError('Invalid EMF input, \'1sec\', \'4sec\', or \'hires\'+'+
                         '\'-\'+\'gei\', \'geo\', \'gse\', \'gsm\', or \'sm\'')

    if not (type(check) is bool):
        raise ValueError('Invalid check input, use boolean')

    if not (type(all) is bool):
        raise ValueError('Invalid all input, use boolean')

    if not (type(TOFxE) is bool):
        raise ValueError('Invalid TOFxE input, use boolean')

    if not (type(TOFxPH) is bool):
        raise ValueError('Invalid TOFxPH input, use boolean')

    if not (type(HOPE) is bool):
        raise ValueError('Invalid HOPE input, use boolean')
        
    if not (type(MagEIS) is bool):
        raise ValueError('Invalid MagEIS input, use boolean')

    if not (type(EMFISIS) is bool):
        raise ValueError('Invalid EMFISIS input, use boolean')
        
        
        
    cdfs = {}
    
	if getenv('PYTHONPATH'):
        localDir = getenv('PYTHONPATH', '')
    else:
        localDir = getenv('LOCALAPPDATA', '')
    
    config = ConfigParser()
    if isfile(join(localDir, 'getCDFsConfig.ini')):
        config.read(join(localDir, 'getCDFsConfig.ini'))
        root = config.get('Directories', 'root')
    else:
        root = normpath(input('Please input a root directory for your cdf files:'))
        config['Directories'] = {'root':root}
        with open(join(localDir,'getCDFsConfig.ini'), 'w') as configfile:
            config.write(configfile)
    
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize: # near the end
                sys.stderr.write("\n")
        else: # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))
    
    if (TOFxPH==True and species=='He'):
        print('There is no He data product for TOFxPH')
        return
    
    if (TOFxE==True or TOFxPH==True or HOPE==True or MagEIS==True or EMFISIS==True):
        all = False
        
    if (all==True):
        TOFxE = True
        if species != 'He':
            TOFxPH = True
        HOPE = True
        MagEIS = True
        EMFISIS = True
        
    def getTOFxE():
        url = 'http://rbspice'+craft.lower()+'.ftecs.com/Level_'+RBlevel+'/TOFxE'+species+'/'+date.strftime('%Y')+'/'
        destination = join(root, craft, 'TOFxE'+species, 'L'+RBlevel)
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No TOFxE file')
                return
            else:
                print('Loading TOFxE...')
                return cdf.CDF(join(destination, file[0]))
        try:
            stat(destination)
        except:
            makedirs(destination, exist_ok=True)
        request = requests.get(url)
        if request.status_code == 404:
            print('Year does not exist for TOFxE'+species+' '+craft)
            return
        page = request.text
        soup = BeautifulSoup(page, 'html.parser')
        files = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.cdf')]
        fileList = filter(files, '*'+date.strftime('%Y%m%d')+'*')
        if not fileList:
            print('Month or day does not exist for TOFxE'+species+' '+craft)
            return
        file = 'http://rbspice'+craft.lower()+'.ftecs.com' + fileList[-1]
        fname = file[file.rfind('/')+1:]
        fnameNoVer = fname[:fname.rfind('v')+1]
        prevFile = filter(listdir(destination), fnameNoVer+'*')
        if prevFile:
            ver = fname[fname.rfind('v')+1:fname.rfind('.')]
            prevVer = prevFile[0][prevFile[0].rfind('v')+1:prevFile[0].rfind('.')]
        else:
            ver = 1
            prevVer = 0
        if ver == prevVer:
            print('Loading TOFxE...')
            return cdf.CDF(join(destination, fname))
        else:
            if prevVer != 0:
                print('Updating TOFxE...')
            else:
                print('Downloading TOFxE...')
            newCDF = cdf.CDF(urlretrieve(file, join(destination, fname), reporthook)[0])
            if prevVer != 0:
                remove(join(destination, prevFile[0]))
            return newCDF

    def getTOFxPH():
        url = 'http://rbspice'+craft.lower()+'.ftecs.com/Level_'+RBlevel+'/TOFxPH'+species+PH+'/'+date.strftime('%Y')+'/'
        destination = join(root, craft, 'TOFxPH'+species, 'L'+RBlevel+'-'+PH)
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No TOFxPH file')
                return
            else:
                print('Loading TOFxPH...')
                return cdf.CDF(join(destination, file[0]))
        try:
            stat(destination)
        except:
            makedirs(destination, exist_ok=True)
        request = requests.get(url)
        if request.status_code == 404:
            print('Year does not exist for TOFxPH'+species+PH+' '+craft)
            return
        page = request.text
        soup = BeautifulSoup(page, 'html.parser')
        files = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.cdf')]
        fileList = filter(files, '*'+date.strftime('%Y%m%d')+'*')
        if not fileList:
            print('Month or day does not exist for TOFxPH'+species+PH+' '+craft)
            return
        file = 'http://rbspice'+craft.lower()+'.ftecs.com' + fileList[-1]
        fname = file[file.rfind('/')+1:]
        fnameNoVer = fname[:fname.rfind('v')+1]
        prevFile = filter(listdir(destination), fnameNoVer+'*')
        if prevFile:
            ver = fname[fname.rfind('v')+1:fname.rfind('.')]
            prevVer = prevFile[0][prevFile[0].rfind('v')+1:prevFile[0].rfind('.')]
        else:
            ver = 1
            prevVer = 0
        if ver == prevVer:
            print('Loading TOFxPH...')
            return cdf.CDF(join(destination, fname))
        else:
            if prevVer != 0:
                print('Updating TOFxPH...')
            else:
                print('Downloading TOFxPH...')
            newCDF = cdf.CDF(urlretrieve(file, join(destination, fname), reporthook)[0])
            if prevVer != 0:
                remove(join(destination, prevFile[0]))
            return newCDF
        
    def getHOPE():
        url = 'https://rbsp-ect.lanl.gov/data_pub/rbsp'+craft.lower()+'/hope/level'+Hlevel
        if Hlevel == '3':
            url = url+'/'+Hproduct+'/'
        destination = join(root, craft, 'HOPE', 'L'+Hlevel+Hproduct)
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No HOPE file')
                return
            else:
                print('Loading HOPE...')
                return cdf.CDF(join(destination, file[0]))
        try:
            stat(destination)
        except:
            makedirs(destination, exist_ok=True)
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        files = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.cdf')]
        fileList = filter(files, '*'+date.strftime('%Y%m%d')+'*')
        if not fileList:
            print('Date does not exist for HOPE '+craft)
            return
        file = url + fileList[-1]
        fname = file[file.rfind('/')+1:]
        fnameNoVer = fname[:fname.rfind('v')+1]
        prevFile = filter(listdir(destination), fnameNoVer+'*')
        if prevFile:
            ver = fname[fname.rfind('v')+1:fname.rfind('.')]
            prevVer = prevFile[0][prevFile[0].rfind('v')+1:prevFile[0].rfind('.')]
        else:
            ver = 1
            prevVer = 0
        if ver == prevVer:
            print('Loading HOPE...')
            return cdf.CDF(join(destination, fname))
        else:
            if prevVer != 0:
                print('Updating HOPE...')
            else:
                print('Downloading HOPE...')
            newCDF = cdf.CDF(urlretrieve(file, join(destination, fname), reporthook)[0])
            if prevVer != 0:
                remove(join(destination, prevFile[0]))
            return newCDF
        
    def getMagEIS():
        url = 'https://rbsp-ect.lanl.gov/data_pub/rbsp'+craft.lower()+'/mageis/level'+Hlevel+'/'
        destination = join(root, craft, 'MagEIS', 'L'+Maglevel)
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No MagEIS file')
                return
            else:
                print('Loading MagEIS...')
                return cdf.CDF(join(destination, file[0]))
        try:
            stat(destination)
        except:
            makedirs(destination, exist_ok=True)
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        files = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.cdf')]
        fileList = filter(files, '*'+date.strftime('%Y%m%d')+'*')
        if not fileList:
            print('Date does not exist for MagEIS '+craft)
            return
        file = url + fileList[-1]
        fname = file[file.rfind('/')+1:]
        fnameNoVer = fname[:fname.rfind('v')+1]
        prevFile = filter(listdir(destination), fnameNoVer+'*')
        if prevFile:
            ver = fname[fname.rfind('v')+1:fname.rfind('.')]
            prevVer = prevFile[0][prevFile[0].rfind('v')+1:prevFile[0].rfind('.')]
        else:
            ver = 1
            prevVer = 0
        if ver == prevVer:
            print('Loading MagEIS...')
            return cdf.CDF(join(destination, fname))
        else:
            if prevVer != 0:
                print('Updating MagEIS...')
            else:
                print('Downloading MagEIS...')
            newCDF = cdf.CDF(urlretrieve(file, join(destination, fname), reporthook)[0])
            if prevVer != 0:
                remove(join(destination, prevFile[0]))
            return newCDF
        
    def getEMFISIS():
        url = 'http://emfisis.physics.uiowa.edu/Flight/RBSP-'+craft+'/L'+EMlevel+'/'+date.strftime('%Y/%m/%d/')
        destination = join(root, craft, 'EMFISIS', 'L'+EMlevel)
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No EMFISIS file')
                return
            else:
                print('Loading EMFISIS...')
                return cdf.CDF(join(destination, file[0]))
        try:
            stat(destination)
        except:
            makedirs(destination, exist_ok=True)
        request = requests.get(url)
        if (request.url == 'http://emfisis.physics.uiowa.edu/data/access_denied'):
            print('Year does not exist for EMFISIS '+craft)
            return
        elif (request.status_code==404):
            print('Month or day does not exist for EMFISIS '+craft)
            return
        page = request.text
        soup = BeautifulSoup(page, 'html.parser')
        files = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.cdf')]
        file = url + filter(files, '*'+EMF+'*'+date.strftime('%Y%m%d')+'*')[-1]
        fname = file[file.rfind('/')+1:]
        fnameNoVer = fname[:fname.rfind('v')+1]
        prevFile = filter(listdir(destination), fnameNoVer+'*')
        if prevFile:
            ver = fname[fname.rfind('v')+1:fname.rfind('.')]
            prevVer = prevFile[0][prevFile[0].rfind('v')+1:prevFile[0].rfind('.')]
        else:
            ver = 1
            prevVer = 0
        if ver == prevVer:
            print('Loading EMFISIS...')
            return cdf.CDF(join(destination, fname))
        else:
            if prevVer != 0:
                print('Updating EMFISIS...')
            else:
                print('Downloading EMFISIS...')
            newCDF = cdf.CDF(urlretrieve(file, join(destination, fname), reporthook)[0])
            if prevVer != 0:
                remove(join(destination, prevFile[0]))
            return newCDF
                
    if (TOFxE==True):
        cdfs['TOFxE'] = getTOFxE()
        if (cdfs['TOFxE'] != None):
            sys.stderr.write('Loaded TOFxE\n')
    else:
        cdfs['TOFxE'] = None
        
    if (TOFxPH==True):
        cdfs['TOFxPH'] = getTOFxPH()
        if (cdfs['TOFxPH'] != None):
            sys.stderr.write('Loaded TOFxPH\n')
    else:
        cdfs['TOFxPH'] = None
        
    if (HOPE==True):
        cdfs['HOPE'] = getHOPE()
        if (cdfs['HOPE'] != None):
            sys.stderr.write('Loaded HOPE\n')
    else:
        cdfs['HOPE'] = None
        
    if (MagEIS==True):
        cdfs['MagEIS'] = getMagEIS()
        if (cdfs['MagEIS'] != None):
            sys.stderr.write('Loaded MagEIS\n')
    else:
        cdfs['MagEIS'] = None
        
    if (EMFISIS==True):
        cdfs['EMFISIS'] = getEMFISIS()
        if (cdfs['EMFISIS'] != None):
            sys.stderr.write('Loaded EMFISIS\n')
    else:
        cdfs['EMFISIS'] = None
        
    return cdfs

def changeRoot():
    '''
    Running this will query you for a new root folder, which will be stored in your config file.
    '''
    from configparser import ConfigParser
    from os.path import normpath, join
    from os import getenv
    
    if getenv('PYTHONPATH'):
        localDir = getenv('PYTHONPATH', '')
    else:
        localDir = getenv('LOCALAPPDATA', '')
    root = normpath(input('Please input a root directory for your cdf files:'))
    
    config = ConfigParser()
    config['Directories'] = {'root':root}
    with open(join(localDir, 'getCDFsConfig.ini'), 'w') as configfile:
        config.write(configfile)



