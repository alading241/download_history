import sys
import os
import time

def get_importitems(imports):
    CURRENTURL = os.path.dirname(os.path.dirname(__file__))


    basepath = r'F:\my'


    localpath = os.path.join(CURRENTURL,'gl')
    if not os.path.exists(localpath):
        os.makedirs(localpath)


    importitems = []



    for im in imports:
        path = os.path.join(basepath,*im[:-1],im[-1]+'.py')
        localfile = os.path.join(localpath,im[-1]+'.py')
        if os.path.exists(path):
            filename = path
            with open(filename,'rb') as f:
                data = f.read()

            filename = localfile
            with open(filename,'wb') as f:
                f.write(data)


        x = __import__('gl.%s'%im[-1])
        importitems.append(getattr(x,im[-1]))
    return importitems

imports = [
            ('F00_myfn','h14_hgcrypto'),
            ('F00_myfn','h13_request'),
            ('F00_myfn','h00_mylittlefunc'),
            ('F00_myfn','h12_save_data'),
            ('F00_myfn','h07_time_interval'),
            ]


importitems = get_importitems(imports)
SavePassword = importitems[0].SavePassword
request_get = importitems[1].request_get
opt_read = importitems[2].opt_read
tryruntime = importitems[2].tryruntime
SaveData = importitems[3].SaveData
Time_interval = importitems[4].Time_interval