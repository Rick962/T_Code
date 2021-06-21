import os
import sys
import json
import time
import gzip
import redis
import websocket
import logging.config

sys.path.append(os.path.dirname(os.getcwd()))
from until.CoinSymbol import tradeStrs
from until.log_setting import logconfig

logging.config.dictConfig(logconfig)
logger = logging.getLogger(__name__)

redisConnect = redis.StrictRedis(host='localhost', port=6379, db=0)


# 数据处理 输入解压后的原始数据、转换成json格式、redis推送
def analys_pub(item):
    try:
        code = ''
        item = json.loads(item)
        if 'tick' in item.keys():
            symbol = item['ch'][7:-11]
            # print(len(symbol))
            if len(symbol) == 7:
                code = symbol[:-4] + '_' + symbol[-4:]
                # print(code)
            elif len(symbol) == 6:
                code = symbol[:-3] + '_' + symbol[-3:]
            name = code.upper()
            # print(name)
            timestamp = item['ts']
            dt = (str(timestamp)[0:10])
            date = time.strftime("%Y-%m-%d", time.localtime(int(dt)))
            times = time.strftime("%H:%M:%S", time.localtime(int(dt)))
            open = item['tick']['open']
            close = item['tick']['close']
            low = item['tick']['low']
            high = item['tick']['high']
            volume = item['tick']['amount']
            try:
                exrate = float(redisConnect.get('ex_rate'))
            except:
                exrate = float(7.00)
            cnyP = close * exrate
            change = close - open
            changeRate = '{:.2%}'.format(change / open)

            dataArr = {
                "code": code,
                "name": name,
                "date": date,
                "time": times,
                "timestamp": timestamp,
                "price": close,
                "cnyPrice": cnyP,
                "open": open,
                "close": close,
                "high": high,
                "low": low,
                "volume": volume,
                "change": change,
                "changeRate": changeRate,
                "buy": 'None',
                "sell": 'None',
            }
            # print(dataArr)
            redisConnect.set('vb:ticker:newprice:' + str(code), close)
            redisConnect.set('vb:ticker:newitem:' + str(code), json.dumps(dataArr))
            redisConnect.publish('vb:ticker:chan:ADEX', json.dumps(dataArr))
    except Exception as e:
        logger.error('处理ticker数据失败：　%s　' % e)


# class Teade_Data():
def spider():
    while True:
        try:
            ws = websocket.create_connection('wss://api.huobiasia.vip/ws', timeout=30)
            break
        except:
            print('connect is error...')
            time.sleep(3)

    tickerStrs = ['{"sub": "market.btcusdt.kline.1day"}',
                  '{"sub": "market.ethusdt.kline.1day"}',
                  '{"sub": "market.xrpusdt.kline.1day"}',
                  '{"sub": "market.ltcusdt.kline.1day"}',
                  '{"sub": "market.bchusdt.kline.1day"}',
                  '{"sub": "market.eosusdt.kline.1day"}',
                  '{"sub": "market.etcusdt.kline.1day"}',
                  '{"sub": "market.ltcbtc.kline.1day"}',
                  '{"sub": "market.bchbtc.kline.1day"}',
                  '{"sub": "market.ethbtc.kline.1day"}',
                  '{"sub": "market.eosbtc.kline.1day"}',
                  '{"sub": "market.eoseth.kline.1day"}',
                  '{"sub": "market.trxeth.kline.1day"}',
                  '{"sub": "market.omgeth.kline.1day"}',
                  '{"sub": "market.xmreth.kline.1day"}',
                  ]

    for tickerStr in tickerStrs:
        ws.send(tickerStr)

    while True:
        try:
            compressData = ws.recv()
            result = gzip.decompress(compressData).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":' + ts + '}'
                ws.send(pong)
                # ws.send('{"sub": "market.btcusdt.kline.1min"}')
            else:
                # print('返回成功')
                # print(result)
                analys_pub(result)
        except Exception as e:
            logger.error('获取返回数据失败：　%s　' % e)
            break


spider()
