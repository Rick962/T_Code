import os
import sys

run = 'python HisData_60min.py'

os.chdir(os.path.dirname(sys.path[0]) + '/Sql_data_his')

while True:
    os.system(run)
