import urllib
def loadPyFile(fileName):
    webFile='https://bitbucket.org/juan_ignacio_garcia_garcia/commutativemonoids/raw/master/'+fileName
    print('downloading...',webFile)
    response=urllib.request.urlopen(webFile)
    content = response.read()
    pos=len(webFile)-webFile[-1::-1].index('/')
    file=open(webFile[pos:],'w')
    file.write(content.decode())
    file.close()

