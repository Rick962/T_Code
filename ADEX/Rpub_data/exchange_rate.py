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
    url = 'https://www.feixiaohao.com/currencies/tether/'
    try:
        rate = pq(url)('.mainPrice')('.convert').eq(0).text()
        par = {"USDT": rate}
        redisConnect.set('vb:indexTickerAll:usd2cny', json.dumps(par))
        redisConnect.set('ex_rate', rate)
        # print(rate,par)
    except:
        redisConnect.set('ex_rate', int(7))
        # continue
        pass

if __name__ == '__main__':
    exchange_rate()
