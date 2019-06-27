
import traceback
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import re
import os
# exit()
currentUrl = os.path.dirname(__file__)
import hashlib
import random

from pprint import pprint



def main():
    url = 'http://127.0.0.1:8000/admin/'
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    opt=None
    driver = webdriver.Chrome(options=opt)

    driver.get(url)

    md5 = None
    while True:
        filename = 'gl/myexec.py'
        try:
            with open(filename,'r',encoding='utf-8') as f:
                data = f.read()
        except:
            time.sleep(3)
            continue

        md5_now = hashlib.md5()   
        md5_now.update(data.encode('utf-8'))
        md5_now = md5_now.hexdigest()
        if md5_now != md5:
            md5 = md5_now
            try:
                exec(data)
            except Exception:
                traceback.print_exc()
        else:
            time.sleep(1)

        

    driver.close()
    driver.quit()

def try_run(fun):
    def inner(*arg,**kw):
        try:
            data = fun(*arg,**kw)
        except:
            traceback.print_exc()
            data = False
        return data
    return inner

if __name__ == '__main__':
    main()