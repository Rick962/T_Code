import time
import json
import redis
import pymysql
import random
from until.db_setting import conn
from until.db_setting import redisConnect
from until.CoinSymbol import coinMap
from until.CoinSymbol import coinPid
from until.CoinSymbol import subChannel


cursor = conn.cursor()


def write_db(data):
    try:
        insert_sql = "REPLACE INTO xy_5min_info(pid, code, name, openingPrice, highestPrice, " \
                     "closingPrice, lowestPrice, volume, date, time, dateTime, timestamp) " \
                     "VALUES ('%d', '%s', '%s', %f, %f, %f, %f, %f, '%s', '%s', '%s', '%s')"
        # print(insert_sql % (data))
        cursor.execute(insert_sql % (data))
        conn.commit()
    except EOFError as e:
        print('write error: %s ', e)
        # logger.error('write error: %s ', e)
    return


p = redisConnect.pubsub()
p.subscribe(subChannel)
while True:
    message = p.listen()
    for i in message:
        if i["type"] == 'message':
            data = i["data"]
            item = json.loads(data)
            code = item['code']
            name = item['name']
            #if code == 'bsv_usdt' or 'dash_usdt' or 'trx_usdt':
            #   pass
            timestamp = int(str(item['timestamp'])[0:10])
            # datetime = time.strftime("%Y-%m-%d %H:%M:00", time.localtime(timestamp))
            # new_time_index = int(time.strftime("%M", time.localtime(int(timestamp))))

            index = int(time.strftime("%M", time.localtime(int(timestamp))))
            new_time_index = index - index % 5
            datetimes = time.strftime("%Y-%m-%d %H:" + str(new_time_index) + ":00", time.localtime(timestamp))
            time_stamp = int(time.mktime(time.strptime(datetimes, "%Y-%m-%d %H:%M:%S")))
            code = item['code']
            # print(code)
            # print(sub_timestamp)
            # indextime = str(new_time_index - new_time_index % 15)

            if coinMap.get(code)['old_time_index'] is None:
                coinMap.get(code)['openprice'] = item['close']
                coinMap.get(code)['closePrice'] = item['close']
                coinMap.get(code)['highprice'] = item['close']
                coinMap.get(code)['lowprice'] = item['close']
                coinMap.get(code)['volume'] = item['volume']
            else:
                if coinMap.get(code)['old_time_index'] != new_time_index:
                    volumes = int(item['volume'] - coinMap.get(code)['volume'])
                    if volumes < 0:
                        #    volumes = int(item['volume'])
                        volumes = abs(int(coinMap.get(code)['volume'] / 288))
                    name = code.upper()
                    pid = coinPid.get(name)
                    timestamp = timestamp - 300
                    datetime = time.strftime("%Y-%m-%d %H:%M:00", time.localtime(timestamp))
                    date = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                    ttime = time.strftime("%H:%M:00", time.localtime(timestamp))

                    # write in SQL
                    if name in coinPid.keys():
                    #else:
                        write_db(
                            (pid, code, name, coinMap.get(code)['openprice'],
                             coinMap.get(code)['highprice'],
                             coinMap.get(code)['closePrice'],
                             coinMap.get(code)['lowprice'],
                             volumes,
                             date, ttime, datetime, timestamp
                             ))
                        #print(code, datetime)
                    coinMap.get(code)['highprice'] = item['close']
                    coinMap.get(code)['lowprice'] = item['close']
                    coinMap.get(code)['openprice'] = item['close']
                    coinMap.get(code)['volume'] = item['volume']

                else:
                    if item['close'] > coinMap.get(code)['highprice']:
                        coinMap.get(code)['highprice'] = item['close']
                    if item['close'] < coinMap.get(code)['lowprice']:
                        coinMap.get(code)['lowprice'] = item['close']
                    coinMap.get(code)['closePrice'] = item['close']
                    volumes = int(item['volume'] - coinMap.get(code)['volume'])
                    if volumes == 0:
                        volumes = 1

                    dataArr = {
                        'type': 'minute5',
                        'code': code,
                        'name': name,
                        'datetime': datetimes,
                        'timestamp': time_stamp,
                        'open': coinMap.get(code)['openprice'],
                        'close': coinMap.get(code)['closePrice'],
                        'high': coinMap.get(code)['highprice'],
                        'low': coinMap.get(code)['lowprice'],
                        'cnyPrice': item['cnyPrice'],
                        'changeRate':item['changeRate'],
                        'volume': volumes,
                    }

                    redisConnect.publish('vb:channel:newkline:minute5', json.dumps(dataArr))
            coinMap.get(code)['old_time_index'] = new_time_index
