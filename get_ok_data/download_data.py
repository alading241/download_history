
import os
import sys
import json
CURRENTURL = os.path.dirname(__file__)
sys.path.append(os.path.dirname(CURRENTURL))

from gl.gl import SavePassword, request_get, opt_read, SaveData

import time
from pprint import pprint
import pickle
from datetime import datetime
from analysis_data import main as analysis
HISTORYURL = 'https://www.okex.me/v3/futures/pc/market/%s/candles?granularity=%s&size=2880'
DATAPATH = r'F:\my\P040_exchange_api\gl\gl\save_data'



def date_to_timestamp(s,end='.000Z'):
    d_time_0 = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S'+end)
    data = int(time.mktime(d_time_0.timetuple()))
    return data


def readdata(filename):
    with open(filename,'rb') as f:
        data = pickle.load(f)
    return data


'''
timestamp   String  开始时间
open    String  开盘价格
high    String  最高价格
low String  最低价格
close   String  收盘价格
volume  String  交易量(张)
currency_volume String  按币种折算的交易量
'''

def get_history(name,file,T):
    url = HISTORYURL % (name,T)
    opt_request_get = opt_read(24 * 60 * 60,pa=file)(request_get)
    data = opt_request_get(url).decode('utf-8')
    data = json.loads(data)
    data = data['data']
    data = [ [date_to_timestamp(da[0])] + [ float(d) for d in da[1:]]  for da in data ]
    return data

def get_history_5min(name,start):
    url = HISTORYURL % (name,300) + '&start=' + start
    # print(url)
    opt_request_get = request_get
    data = opt_request_get(url).decode('utf-8')
    data = json.loads(data)
    data = data['data']
    data = [ [date_to_timestamp(da[0])] + [ float(d) for d in da[1:]]  for da in data if date_to_timestamp(da[0]) > date_to_timestamp(start,'Z') - 300]
    return data

def get_currency_name():
    url = 'https://www.okex.me/api/futures/v3/instruments'
    opt_request_get = opt_read(60 * 60 * 3,pa='instruments')(request_get)
    data = opt_request_get(url).decode('utf-8')
    data = json.loads(data)
    data = [ (da['instrument_id'],da['underlying_index'].lower() + '_' + da['alias']) for da in data]
    return data








def get_future_data(data):
    period_names = ('15min' ,'30min' ,'1hour' ,'2hour' ,'4hour' ,'6hour' ,'12hour' ,'1day' ,'1week')
    periods = (900,1800,3600,7200,14400,21600,43200,86400,604800)


    # 重新下载数据的时候需要 注销这句
    period_names = ()

    for name,T in data:
        try:


            filepath = os.path.join(DATAPATH,T)
            if not os.path.exists(filepath):
                os.makedirs(filepath)

            

            print(filepath,end='\r')
            for period_name,period in zip(period_names,periods):
                print(filepath,period_name,end='\r')
                filename = os.path.join(filepath,period_name)
                if not os.path.exists(filename):
                    data = get_history(name, T+period_name, period)
                    time.sleep(1)
                    with open(filename,'wb') as f:
                        pickle.dump(data,f)

            sd = SaveData(T,merge_name='300k',merge_size=1000 * 300)
            if sd.index == 0:
                data = get_history(name, T+'5min', 300)
                sd.save_data(data)
            else:
                data = sd.get_last_data()
                date = data[-1][0]
                if time.time() - date > 16 * 3600:
                    start = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime(date + 300))
                    data = get_history_5min(name,start)
                    if (data[0][0]) != date+300:
                        print(filepath,'     ')
                        raise ValueError('时间不相等 %s %s' % (data[0][0] , date + 300))
                    sd.save_data(data)
        except:
            print(name,T)

def main():
    global HISTORYURL


    data = get_currency_name()

    get_future_data(data)

    # 下载现货
    HISTORYURL = 'https://www.okex.me/api/index/v3/instruments/%s/candles?granularity=%s&size=2880'
    data = [
            ('BTC-USD','btc_now'),
            ('BCH-USD','bch_now'),
            ('BSV-USD','bsv_now'),
            ('EOS-USD','eos_now'),
            ('ETH-USD','eth_now'),
            ('ETC-USD','etc_now'),
            ('LTC-USD','ltc_now'),
            ('TRX-USD','trx_now'),
            ('XRP-USD','xrp_now'),
            ]
    get_future_data(data)

    # 分析数据
    analysis()

    input('输入任何键进行关闭')

if __name__ == '__main__':
    main()

        # start = 
        # exit()
    # sd.save_data(data)


# data = readdata(r'F:\my\P040_exchange_api\gl\gl\__opt_read\bch_next_week5min.dat')
# pprint(json.loads(data.decode('utf-8'))['data'][-1])

