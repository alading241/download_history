import os
from pprint import pprint
import pickle
from gl.gl import tryruntime,Time_interval,SaveData

CURRENTURL = os.path.dirname(__file__)
BASEPATH = os.path.dirname(CURRENTURL)
BASEDATA = os.path.join(BASEPATH,'gl','gl','save_data')
PERIOD_NAMES = ('15min' ,'30min' ,'1hour' ,'2hour' ,'4hour' ,'6hour' ,'12hour' ,'1day' ,'1week')
PERIODS = (900,1800,3600,7200,14400,21600,43200,86400,604800)
PERIODDICT = dict(zip(PERIOD_NAMES,PERIODS))

def analysis(file,period,lastda=None):
    with open(file,'rb') as f:
        data = pickle.load(f)
    if lastda and data[0][0]-lastda[0] != period:
        raise ValueError('数据连接处有问题 \n%s \n%s %s %s' % (file, lastda[0], data[0][0],(data[0][0]-lastda[0])/period))

    lastda = data[0]
    err = []
    for da in data[1:]:
        if lastda[0] + period != da[0]:
            # raise ValueError
            err.append('数据不连续 \n%s \n%s %s %s' % (file, lastda[0], da[0],(da[0]-lastda[0])/period))
            if da[0]-lastda[0] < 0 or da[0]-lastda[0] > period:
                raise ValueError('数据不连续 \n%s \n%s %s %s' % (file, lastda[0], da[0],(da[0]-lastda[0])/period))
        lastda = da
    else:
        print('数据正确', file, end='\r')

    if err:
        print(file,len(err),'--')

    return len(err),lastda


def main():
    '检查数据断点处的连续性'
    paths = []
    for path in os.listdir(BASEDATA):
        if os.path.isdir(os.path.join(BASEDATA,path)):
            paths.append(path)

    errsum = 0
    errnum = 0
    for path in paths:
        filelst = os.listdir(os.path.join(BASEDATA,path))
        for file in filelst:
            period = PERIODDICT.get(file)
            if period:
                '先不处理 显示数据的时候进行处理'
                continue

                file = os.path.join(BASEDATA,path,file)
                num, _ = analysis(file,period)
                errsum += num
                if num:
                    errnum += 1

        lastda = None
        filelst = list(filter(lambda x:x.isdigit(),filelst))
        filelst.sort(key = lambda x:int(x))
        for file in filelst:
            file = os.path.join(BASEDATA,path,file)
            _, lastda = analysis(file,300,lastda)

    print(errsum,errnum,'|-|')



def check_data_continue():
    '检擦数据的连续型'
    pathlst = os.listdir('gl/gl/save_data')

    for T in pathlst:
        sd = SaveData(T,merge_name='300k',merge_size=1000 * 300)

        data = sd.get_all_the_index_data()

        print(T,len(data),len(data)/(12 * 24),end='\r')


        lastda = data[0]
        for da in data[1:]:
            if da[0] - lastda[0] != 300:
                raise ValueError(da[0], lastda[0], da[0] - lastda[0])
            else:
                print('ok',end='\r')
            lastda = da



if __name__ == '__main__':
    main()
