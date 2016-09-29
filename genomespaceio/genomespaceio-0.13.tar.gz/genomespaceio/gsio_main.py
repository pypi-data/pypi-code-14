"""This is the GenomeSpace Input/Output (genomespaceiO) module.

This module lets you login to GenomeSpace, upload and download files. For sonme files (gct and things that can convert to it)
it lets you get the contents as a Pandas data frame
"""
__version__ = '0.1'
__author__ = 'Ted Liefeld'


import requests
from requests.auth import HTTPBasicAuth
from requests.cookies import RequestsCookieJar
import pandas
from io import StringIO

class GenomeSpaceIO() :
    
     def __init__(self, gsuser=None, gspass=None):
        if ((len(gsuser) == 0 ) or (len(gspass) == 0)):
            raise Exception("GenomeSpace Username or password is missing for some odd reason.")

        # save the username, we'll ened it for uploads (possibly) but not the password    
        self.gsusername = gsuser
        # set up a cookie jar to have a gs-token cookie after login.  The cookie will authenticate subsequent
        # calls to GenomeSpace so that we do not need to keep the password around
        self.jar = requests.cookies.RequestsCookieJar()    
        self.login(gspass);
        
        
     def login(self, apass):
         """
         klkjjj
         """
         url = "https://"+self.gsusername + ":" + apass + "@identity.genomespace.org/identityServer/selfmanagement/user"
         response = requests.get(url)
                
         if (response.status_code == 200):
             userInfo = response.json()
             username2 = userInfo['username']
             self.jar.set('gs-token', userInfo['token'])
             print("... Connected successfully to GenomeSpace as ",  username2)
         else:
            raise Exception("Failed to connect to GenomeSpace.  Status code: ", response.status_code)

     def get_GS_URL(self, url):
        response = requests.get(url, allow_redirects=True, cookies=self.jar)
        return response
         
     def download_GS_URL_to_file(self, url):
        # get the filename from the end of the URL or path
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True, allow_redirects=True, cookies=self.jar)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename    
         
     def __get_file_size(self, filename):
        fileobject = open(filename, 'rb')
        fileobject.seek(0,2) # move the cursor to the end of the file
        size = fileobject.tell()
        return size
        
     def get_GS_URL_as_Frame(self, url):
        format = url.split('.')[-1].lower()
        if (format != "gct"):
            allowedFormats = [];
            canConvert = False
            formatUrl = ''
            dm_fc_url = 'https://dm.genomespace.org/datamanager/v1.0/dataformatconverter/list';
            response = self.get_GS_URL(dm_fc_url)
            x = response.json()
           
            for fc in x:
                #print (fc['inputFormat']['fileExtension'], " to ", fc['outputFormat']['fileExtension'])
                if fc['outputFormat']['fileExtension'] == 'gct':
                    allowedFormats.append(fc['inputFormat']['fileExtension'])
                    if (fc['inputFormat']['fileExtension'] == format):
                        print ("we can convert from ", fc['inputFormat']['fileExtension'], " to ", fc['outputFormat']['fileExtension'])
                        formatUrl = fc['outputFormat']['url']
                        canConvert = True
            
            if (canConvert):
                url = url + '?dataformat=' + formatUrl
            else:
                raise Exception("For now can only present gct files as a frame or a format that GS can convert to gct: " + ', '.join(allowedFormats))
                return;
        print("... Downloading : ", url)    
        response = self.get_GS_URL(url)
        
        #reads all into memory
        data_io = StringIO(response.text)

        # This reads the file and generates data structure representing the values.
        # If a code cell returns this value, it will be displayed in the notebook as a table.
        # The parameters are as follows:
        #
        #     delimiter:   GCT files are tab-separated
        #     header:      This line contains the column headers
        return pandas.read_csv(data_io, delimiter='\t', header=2, index_col=[0,1], skip_blank_lines=True)
        

        
     def write_gct_file(self, filename, col_names, row_names, row_descrips, matrix):
        f = open(filename, 'w')
        f.write("#1.2\n")
        f.write(str(len(row_names)))
        f.write("\t")
        f.write(str(len(col_names)))
        f.write("\n")
        f.write("Name\tDescription")
        for cname in col_names:
            f.write("\t")
            f.write(cname)
        f.write("\n")
        
        for i, val in enumerate(row_names):
            f.write(val)
            f.write("\t")
            f.write(row_descrips[i])
            
            for j, pval in enumerate(matrix[i]):
                f.write("\t")
                f.write(str(pval))
            f.write("\n")
        
        f.close()
        
        
     def upload_file_to_genomespace(self, filename, dest_path_and_name):
        with open(filename) as fh:
            data = fh.read()
            self.upload_data_to_genomespace(dest_path_and_name, data)
        
        
        
        
        
     def upload_data_to_genomespace(self, dest_path_and_name, data):
        fileLen = str(len(data))
        uploadUrl1 = "https://dm.genomespace.org/datamanager/v1.0/uploadurl/users/"+self.gsusername+"/"+dest_path_and_name+"?Content-Length="+fileLen+"&Content-Type=text/plain"
        resp = self.get_GS_URL(uploadUrl1);
        secondUrl = resp.text
        print(secondUrl)
        
        filepath = 'testout.gct'
        resp2 = requests.put(secondUrl,
                    data=data,                         
                    headers={'content-type':'text/plain', 'content-length': fileLen})
        if (resp2.status_code == 200):
            print("File ("+dest_path_and_name+") successfully uploaded to GenomeSpace")
        else:
            raise Exception("File upload failed ("+dest_path_and_name+"): status: " + resp2.status_code)
            
           

        
        
        
        