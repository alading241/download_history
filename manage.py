from get_ok_data.download_data import main as download_data
from gl.gl import tryruntime,Time_interval



download_data = tryruntime(download_data,sleep_time=60 * 20)




a2 = Time_interval(download_data,60 * 60 * 24)
while True:
    a2.run()
