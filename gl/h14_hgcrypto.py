from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import hashlib
import json
import getpass
import re
import os
CURRENTURL = os.path.dirname(__file__)


# 加密解密
class HgCrypto(object):
    def __init__(self, arg = None):
        self.cipher = None
        self.arg = arg
        if arg == None:
            self.arg = getpass.getpass("F_Please input your password:")
        self.set_password(self.arg)
        
    def encrypt(self,text):
        encrypted_text = self.cipher.encrypt(text.encode('utf-8'))
        return encrypted_text.decode('utf-8')

    def decrypt(self,encrypted_text):
        decrypted_text = self.cipher.decrypt(encrypted_text.encode('utf-8')).decode('utf-8')
        return decrypted_text

    def set_password(self,str_input = None):
        if str_input == None:
            str_input = input("s_Please input your password:")
        sha1 = hashlib.sha1()
        sha1.update(str_input.encode())
        cipher_key = b'hg_' + sha1.hexdigest().encode() + b'='
        self.cipher = Fernet(cipher_key)

# 加密数据到文件 进行下次解密读取
class SavePassword(HgCrypto):
    def __init__(self):
        self.cipher = None

    def savecrypto(self, filename='pwd'):
        # 只再第一次有作用
        filename = os.path.join(CURRENTURL,filename)
        if os.path.exists(filename):
            print('%s文件已存在 从设请删除' % filename, end = '\r')
            return
            # raise ValueError('%s：已经存在请先删除' % filename)

        if pwd or not self.cipher:
            self.set_password(pwd)
        data = self.encrypt(getpass.getpass("请输入所要加密的字符串:"))
        with open(filename,'w',encoding='utf-8') as f:
            f.write(data)

    def readcrypto(self, pwd=None, filename='pwd'):
        if not os.path.exists(os.path.join(CURRENTURL,filename)):
            self.savecrypto(pwd, filename)
        filename = os.path.join(CURRENTURL,filename)
        with open(filename,'r',encoding='utf-8') as f:
            data = f.read()
        if pwd or not self.cipher:
            self.set_password(pwd)
        try:
            data = self.decrypt(data)
            return data
        except InvalidToken:
            print('密码错误')


def main():
    data = SavePassword().readcrypto('miss')
    print(data)
    data = SavePassword().readcrypto()
    print(data)

if __name__ == '__main__':
    main()