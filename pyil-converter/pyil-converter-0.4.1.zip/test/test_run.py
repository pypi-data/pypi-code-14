import pyil.file
import subprocess
subprocess.Popen(r'..\test.bat')

with pyil.file.text_file('abc.txt','abc') as f:
    print(f.text,'a')
    print(f._ftext,'a')
    print(f.text, 'a')
    f.write('hi1')
    print(f._ftext)
    print(f.text)
