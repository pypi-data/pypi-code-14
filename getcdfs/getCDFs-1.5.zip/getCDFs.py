
# coding: utf-8

# In[3]:

def getCDFs(date, craft, species, PH='LEHT', EMF='1sec-sm', check=True,
            all=True, TOFxE=False, TOFxPH=False, HOPE=False, EMFISIS=False):
    '''
    getCDFs(getCDFs(datetime, string, string, **kw):

    date: Python datetime object containing the date that you want cdfs for.
    craft: character: 'A' or 'B'.
    species: character: 'H', 'He', or 'O'.
    PH: string describing which Time of Flight by Pulse Height product you want: 'LEHT'(Low Energy, High Time resolution) or 'HELT'(High Energy, Low Time resolution).
    EMF: string describing which EMFISIS product you want: ('1sec', '4sec', or 'hires')+'-'+('gei', 'geo', 'gse', 'gsm', or 'sm').
    check: When True, it will query the server for updated versions, if it is False, then the server will not be queried at all. If you don't have the file on your computer, it will not be downloaded. Set this keyword to False if you do not have internet access.
    The last five keywords describe which data product you want, all is default, but if you set any one or more of them to True, then you will only get what you set to True.

    Returns: Python dictionary containing spacepy cdf objects. Keys are 'TOFxE', 'TOFxPH', 'HOPE', and 'EMFISIS'
    '''
    
    cdfs = {}
    
    import sys
    import requests
    from os.path import isfile, sep, normpath
    from os import remove, listdir, stat, makedirs
    from fnmatch import filter
    from bs4 import BeautifulSoup
    from urllib.request import urlretrieve
    import spacepy.pycdf as cdf
    from configparser import ConfigParser
    
    config = ConfigParser()
    if isfile('getCDFsConfig.ini'):
        config.read('getCDFsConfig.ini')
        root = config.get('Directories', 'root')
    else:
        root = normpath(input('Please input a root directory for your cdf files:'))
        config['Directories'] = {'root':root}
        with open('getCDFsConfig.ini', 'w') as configfile:
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
    
    if (TOFxE==True or TOFxPH==True or HOPE==True or EMFISIS==True):
        all = False
        
    if (all==True):
        TOFxE = True
        if species != 'He':
            TOFxPH = True
        HOPE = True
        EMFISIS = True
        
    def getTOFxE():
        url = 'http://rbspice'+craft.lower()+'.ftecs.com/Level_3PAP/TOFxE'+species+'/'+date.strftime('%Y')+'/'
        destination = root+sep+craft+sep+'TOFxE'+species+sep
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No TOFxE file')
                return
            else:
                print('Loading TOFxE...')
                return cdf.CDF(destination+file[0])
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
            return cdf.CDF(destination+fname)
        else:
            if prevVer != 0:
                print('Updating TOFxE...')
            else:
                print('Downloading TOFxE...')
            newCDF = cdf.CDF(urlretrieve(file, destination+fname, reporthook)[0])
            if prevVer != 0:
                remove(destination+prevFile[0])
            return newCDF

    def getTOFxPH():
        url = 'http://rbspice'+craft.lower()+'.ftecs.com/Level_3PAP/TOFxPH'+species+PH+'/'+date.strftime('%Y')+'/'
        destination = root+sep+craft+sep+'TOFxPH'+species+PH+sep
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No TOFxPH file')
                return
            else:
                print('Loading TOFxPH...')
                return cdf.CDF(destination+file[0])
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
            return cdf.CDF(destination+fname)
        else:
            if prevVer != 0:
                print('Updating TOFxPH...')
            else:
                print('Downloading TOFxPH...')
            newCDF = cdf.CDF(urlretrieve(file, destination+fname, reporthook)[0])
            if prevVer != 0:
                remove(destination+prevFile[0])
            return newCDF
        
    def getHOPE():
        url = 'https://rbsp-ect.lanl.gov/data_pub/rbsp'+craft.lower()+'/hope/level3/PA/'
        destination = root+sep+craft+sep+'HOPE'+sep
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No HOPE file')
                return
            else:
                print('Loading HOPE...')
                return cdf.CDF(destination+file[0])
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
            return cdf.CDF(destination+fname)
        else:
            if prevVer != 0:
                print('Updating HOPE...')
            else:
                print('Downloading HOPE...')
            newCDF = cdf.CDF(urlretrieve(file, destination+fname, reporthook)[0])
            if prevVer != 0:
                remove(destination+prevFile[0])
            return newCDF
        
    def getEMFISIS():
        url = 'http://emfisis.physics.uiowa.edu/Flight/RBSP-'+craft+'/L3/'+date.strftime('%Y/%m/%d/')
        destination = root+sep+craft+sep+'EMFISIS'+sep
        if not check:
            file = filter(listdir(destination), '*'+date.strftime('%Y%m%d')+'*')
            if not file:
                print('No EMFISIS file')
                return
            else:
                print('Loading EMFISIS...')
                return cdf.CDF(destination+file[0])
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
            return cdf.CDF(destination+fname)
        else:
            if prevVer != 0:
                print('Updating EMFISIS...')
            else:
                print('Downloading EMFISIS...')
            newCDF = cdf.CDF(urlretrieve(file, destination+fname, reporthook)[0])
            if prevVer != 0:
                remove(destination+prevFile[0])
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
    from os.path import normpath
    root = normpath(input('Please input a root directory for your cdf files:'))
    
    config = ConfigParser()
    config['Directories'] = {'root':root}
    with open('getCDFsConfig.ini', 'w') as configfile:
        config.write(configfile)


# In[ ]:



