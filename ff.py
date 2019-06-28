

from gl.gl import tryruntime,Time_interval,SaveData
from pprint import pprint
import os

import sys
sys.path.insert(1,r'F:\my')
from P038_kline import cl_kline

T = 'eos_next_week'

pathlst = os.listdir('gl/gl/save_data')

for T in pathlst:
    sd = SaveData(T,merge_name='300k',merge_size=1000 * 300)

    data = sd.get_all_the_index_data()

    cl_kline(data[:6])

    exit()