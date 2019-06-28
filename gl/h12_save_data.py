
'保存数据 大于5k数据的移动 不会影响程序运行'
'历史记录只读取了小于5k的数据 接下来需要获取特定index后面的数据了'
'按条保存数据 每次save_data 保存一次数据'
'保存前先判断是否需要合并 至少需要10条记录才会进行合并操作'
import os
import inspect
import sys
from pprint import pprint
import pickle
import traceback
CURRENTURL = os.path.dirname(__file__)

def runfilepath(*path):
    x = inspect.stack()[-1]
    return os.path.join(os.path.dirname(x.filename),*path)

class SaveData(object):
    def __init__(self,filename,main_path='save_data',merge_name='5k',merge_size=5000):
        self.main_path = main_path
        self.filename = filename
        self.path = self.get_path()
        self.min = None
        self.max = None
        self.index = self.get_index()
        self.merge_name = merge_name
        self.merge_size = merge_size
        self.merge_name_lst = ['5k','50k','500k','5M']

    def get_path(self):
        '获得路径'
        # abspath = runfilepath('gl')
        abspath = os.path.join(CURRENTURL, 'gl', self.main_path)
        abspath = os.path.join(abspath,self.filename)
        if not os.path.exists(abspath):
            os.makedirs(abspath)
        return abspath

    def get_index(self):
        '获得编号'
        lst = os.listdir(self.path)
        lst = filter(lambda x: x.isdigit(),lst)
        lst = list(map(lambda x:int(x),lst))
        lst.sort()
        self.data_size_dict = {i:os.path.getsize(os.path.join(self.path,'%05d' % i)) for i in lst}
        if not lst:
            return 0
        self.min = min_ = min(lst)
        self.max = max_ = max(lst)
        diff = max_ - min_ + 1
        length = len(lst)
        if diff != length:
            raise ValueError('-------------------数据错误-------------------\n%s' % lst)
        return max_


    def save_data(self,data):
        '保存数据'
        try:
            self.merge_data()
        except Exception:
            traceback.print_exc()

        self.index += 1
        filename = os.path.join(self.path, '%05d' % self.index)
        with open(filename,'wb') as f:
            pickle.dump(data,f)
        self.data_size_dict[self.index] = os.path.getsize(filename)
        
    def merge_data(self):
        '数据合并'
        # sum_ = self.get_data_size_dict_size()
        # if sum_ < 5000:
        #     return
        name = self.merge_name
        size = self.merge_size

        if len(self.data_size_dict) < 10:
            return 

        sortdata = sorted(self.data_size_dict.items())

        start = end = sortdata[0][0]
        sum_ = 0
        for item in sortdata:
            
            if end != item[0]:
                raise ValueError('出现了遗漏的数据')
            sum_ += item[1]
            end += 1
            if sum_ > size:
                break
        else:
            return

        filename = os.path.join(self.path , ('%s_%04d_%s' % (name,end-1,end-start)))
        with open(filename,'wb') as ff:
            for i in range(start,end):
                filename = os.path.join(self.path,'%05d' % i)
                with open(filename,'rb') as f:
                    data = pickle.load(f)
                    pickle.dump(data,ff)
                del self.data_size_dict[i]
                os.remove(filename)

    def get_last_data(self):
        filename = os.path.join(self.path,'%05d' % self.index)
        with open(filename,'rb') as f:
            data = pickle.load(f)
        return data

    def get_all_the_index_data(self,isadd=True):
        '获得所有未压缩数据'
        lst = os.listdir(self.path)
        lst = list(filter(lambda x: x.isdigit(),lst))
        lst.sort(key=lambda x:int(x))
        data = []

        if isadd:
            for l in lst:
                data.extend(self.get_data_from_file(l))
        else:
            for l in lst:
                data.append(self.get_data_from_file(l))
        return data

    def get_data_from_file(self,file):
        filename = os.path.join(self.path,file)
        with open(filename,'rb') as f:
            data = pickle.load(f)
        return data

    '这两个函数貌似没有用上 大于5k的合并没有进行'
    def get_merge_path(self,merge_index=0):
        merge_name = self.merge_name_lst[merge_index]
        paths = os.listdir(self.path)
        paths = filter(lambda x: x.startswith(merge_name),paths)
        if not list(paths):
            return
        print(list(paths))

        # print(sum_,start,end)

        # pprint(sortdata)

    def get_data_size_dict_size(self):
        xx = self.data_size_dict.items()
        totle = sum(self.data_size_dict.values())
        return totle

def main():
    sd = SaveData('mysqldata')
    # sd.get_merge_path()

    sd.save_data(1)
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,11000)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))
    # sd.save_data(list(range(1,100)))
    # sd.save_data(list(range(1,1100)))


    # i = 0
    # filename = 'xxxxxxxxx.dat'
    # try:
    #     with open(filename,'rb') as ff:
    #         while True:
    #             i += 1
    #             filename = os.path.join(sd.path,str(i))
    #             with open(filename,'rb') as f:
    #                 data = pickle.load(f)
    #             if data == pickle.load(ff):
    #                 print('==')
    #             else:
    #                 print('!=',i)
    # except Exception:
    #     print(i)


if __name__ == '__main__':
    main()



# 5m_0_最后的id
# 500k_0_最后的id
# 50k_0_最后id
# 5k_0_最后id
# 0 开始

