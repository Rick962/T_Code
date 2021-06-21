import os
import sys

run_ticker = 'python ticker.py'

os.chdir(os.path.dirname(sys.path[0]) + '/Rpub_data')

while True:
    try:
        os.system(run_ticker)
    except:
        print('推送ticker数据失败')
