import time
import json
import redis
import datetime
import pymysql
#import dateutil
#import dateutil.relativedelta
from until.db_setting import conn
from until.CoinSymbol import coinPid
from until.CoinSymbol import coinList
from until.db_setting import redisConnect



cursor = conn.cursor()


def write_db(data):
    try:
        insert_sql = "REPLACE INTO xy_month_info(pid, code, name, openingPrice, highestPrice, " \
                     "closingPrice, lowestPrice, volume, date, time, dateTime, timestamp) " \
                     "VALUES ('%d', '%s', '%s', %f, %f, %f, %f, %f, '%s', '%s', '%s', '%s')"
        # print(insert_sql % (data))
        cursor.execute(insert_sql % (data))
        conn.commit()
    except EOFError as e:
        print('write error: %s ', e)
        # logger.error('write error: %s ', e)
    return


def genKlineDay(coin, datee):
    select_openP = 'select openingPrice from xy_dayk_info where date>='"'" + str(
        datee) + "'"'and code='"'" + str(coin) + "'"' order by timestamp asc limit 1;'
    select_closeP = 'select closingPrice from xy_dayk_info where date>='"'" + str(
        datee) + "'"'and code='"'" + str(coin) + "'"' order by timestamp desc limit 1;'
    select_highP = 'select max(highestPrice) from xy_dayk_info where date>='"'" + str(
        datee) + "'"'and code='"'" + str(coin) + "';"
    select_lowP = 'select min(lowestPrice) from xy_dayk_info where date>='"'" + str(
        datee) + "'"'and code='"'" + str(coin) + "';"
    volumeCount = 'select sum(volume) from xy_dayk_info where date>='"'" + str(
        datee) + "'"'and code='"'" + str(coin) + "';"
    # datetime = 'select date from xy_30min_info where date='"'"+str(datee)+"'"'and code='"'"+str(coin)+"'"' order by timestamp asc limit 1;'

    cursor.execute(select_openP)
    openPrice = float(cursor.fetchone()[0])
    cursor.execute(select_closeP)
    closePrice = float(cursor.fetchone()[0])
    cursor.execute(select_highP)
    highPrice = float(cursor.fetchone()[0])
    cursor.execute(select_lowP)
    lowPrice = float(cursor.fetchone()[0])
    cursor.execute(volumeCount)
    volume = int((cursor.fetchone()[0]))

    name = coin.upper()
    pid = coinPid.get(name)
    timeArray = time.strptime(datee, "%Y-%m-%d")
    time_stamp = int(time.mktime(timeArray))
    ttime = time.strftime("%H:%M:00", time.localtime(time_stamp))
    datetime = time.strftime("%Y-%m-%d 00:00:00", time.localtime(time_stamp))

    # print(openPrice, closePrice, highPrice, lowPrice, volume, datee, datee, datee)

    #print(datee, time_stamp)
    dataArr = {
        'type':'month',
        'code': coin,
        'datetime': str(datee),
        'timestamp': time_stamp,
        'open': openPrice,
        'close': closePrice,
        'high': highPrice,
        'low': lowPrice,
        'volume': volume,
    }
    # print(dataArr)
    # redisConnect.publish('vb:klinemon:chan:test', json.dumps(dataArr))
    redisConnect.set('vb:newklinemon:' + str(coin), json.dumps(dataArr))
    if name in coinPid.keys():
        write_db((pid, coin, name, float(openPrice), float(highPrice), float(closePrice), float(lowPrice), int(volume),
              datee, ttime, datetime, time_stamp))


timestamp = str(time.time())[0:10]
today = time.strftime("%Y-%m-01", time.localtime(int(timestamp)))

# coinList = ['btc_usdt', 'eth_usdt', 'etc_usdt', 'bch_usdt', 'eos_usdt', 'ltc_usdt', 'xrp_usdt', ]
coinList = ['btc_usdt', 'eth_usdt', 'etc_usdt', 'bch_usdt', 'eos_usdt', 'ltc_usdt', 'xrp_usdt', 'coin_usdt', 'btrt_usdt', 'libra_usdt']

for coin in coinList:
    genKlineDay(coin, today)


cursor.close()
conn.close()

# 0 0 1 * * /usr/bin/python /home/data/GIC/Sql_data_his/HisData_1day.py


# 0 1 * * * /usr/bin/python /home/data/LV/genkline_v2/day.py
# 5 0 * * 7 /usr/bin/python /home/data/LV/genkline_v2/week.py
# 0 0 1 * * /usr/bin/python /home/data/LV/genkline_v2/month.py
