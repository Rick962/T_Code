import os
import sys
import json
import time
import requests
import redis
import websocket
import logging.config

sys.path.append(os.path.dirname(os.getcwd()))
from until.CoinSymbol import depthStrs
from until.log_setting import logconfig

logging.config.dictConfig(logconfig)
logger = logging.getLogger(__name__)

redisConnect = redis.StrictRedis(host='localhost', port=6379, db=0)

def exchange_rate():
    url = 'https://www.okex.me/v2/futures/market/indexTickerAll.do'
    while True:
        try:
            mes = json.loads(requests.get(url).text)['data']
            rate = float(mes[2]['usdCnyRate'])
            redisConnect.set('ex_rate', rate)
            rate_dict = '{"USDT":' + str(rate) + '}'
            redisConnect.set('vb:indexTickerAll:usd2cny', rate_dict)
        except Exception as e:
            logger.error(e)
            break
        time.sleep(600)


if __name__ == '__main__':
    exchange_rate()
