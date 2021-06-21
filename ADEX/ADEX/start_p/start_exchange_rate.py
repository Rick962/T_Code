import os
import sys

run_depth_pct = 'python exchange_rate.py'

os.chdir(os.path.dirname(sys.path[0]) + '/Rpub_data')

while True:
    try:
        os.system(run_depth_pct)
    except:
        print('推送depth数据失败')
