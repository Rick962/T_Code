#!/bin/sh


cd start_p

python start_depth.py &
python start_exchange_rate.py &
python start_ticker.py &
python startz_sql_1min.py &
python startz_sql_5min.py &
python startz_sql_15min.py &
python startz_sql_30min.py &
python startz_sql_60min.py &
python startz_sql_1day.py &
python startz_sql_1week.py &
python startz_sql_1mon.py &

# sh RunProject.sh  执行z



