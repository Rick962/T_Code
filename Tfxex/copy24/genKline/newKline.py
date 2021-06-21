import time
import json
import redis
import pymysql
import datetime
from until.db_setting import conn
from until.CoinSymbol import coinPid
from until.CoinSymbol import coinList
from until.CoinSymbol import subChannel
from until.db_setting import redisConnect


# redisConnect = redis.StrictRedis(host='172.31.52.37', port=6379, db=0, password='B8Zl5h456rOHTvuT')


p = redisConnect.pubsub()
p.subscribe(subChannel)
while True:
    message = p.listen()
    for i in message:
        if i["type"] == 'message':
            data = i["data"]
            tickers_item = json.loads(data)
            #print(tickers_item)

            klineweek = redisConnect.get('vb:newklineweek:' + str(tickers_item['code']))
            data = json.loads(klineweek)
            now = datetime.date.today()
            this_week_start = now - datetime.timedelta(days=now.weekday())
            week_day_start = (this_week_start + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            timeArray = time.strptime(week_day_start, "%Y-%m-%d")
            time_stamp = int(time.mktime(timeArray))

            data['timestamp'] = time_stamp
            data['datetime'] = week_day_start
            data['open'] = data['close']
            data['name'] = tickers_item['name']
            if float(tickers_item['close']) > data['high']:
                data['high'] = tickers_item['close']
            if float(tickers_item['close']) < data['low']:
                data['low'] = tickers_item['close']
            data['close'] = tickers_item['close']
            #data['volume'] = data['volume'] + tickers_item['volume']
            redisConnect.publish('vb:channel:newkline:week', json.dumps(data))

            klinemon = redisConnect.get('vb:newklinemon:' + str(tickers_item['code']))
            data = json.loads(klinemon)
            currentTimeStamp = time.time()
            data['datetime'] = time.strftime("%Y-%m-01", time.localtime(currentTimeStamp))
            data['timestamp'] = int(time.mktime(time.strptime(data['datetime'], "%Y-%m-%d")))
            data['open'] = data['close']
            data['name'] = tickers_item['name']

            if float(tickers_item['close']) > data['high']:
                data['high'] = tickers_item['close']
            if float(tickers_item['close']) < data['low']:
                data['low'] = tickers_item['close']
            data['close'] = tickers_item['close']
            # data['volume'] = data['volume'] + tickers_item['volume']
            redisConnect.publish('vb:channel:newkline:month', json.dumps(data))
