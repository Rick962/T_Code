import os
import sys
import json
import time
import gzip
import redis
import websocket
import logging.config

sys.path.append(os.path.dirname(os.getcwd()))
from until.CoinSymbol import depthStrs
from until.log_setting import logconfig

logging.config.dictConfig(logconfig)
logger = logging.getLogger(__name__)

redisConnect = redis.StrictRedis(host='localhost', port=6379, db=0)

btcusdt = {}
ethusdt = {}
xrpusdt = {}
ltcusdt = {}
bchusdt = {}
eosusdt = {}
etcusdt = {}
ltcbtc = {}
bchbtc = {}
ethbtc = {}
eosbtc = {}
eoseth = {}
trxeth = {}
omgeth = {}
xmreth = {}


class Teade_Data:
    def spider(self):
        while True:
            try:
                ws = websocket.create_connection('wss://api.huobiasia.vip/ws', timeout=30)
                break
            except Exception as e:
                logging.error('Websocekt链接: %s  ' % e)
                time.sleep(1)

        depthStrs = [
            '{"sub": "market.btcusdt.depth.step0"}',
            '{"sub": "market.ethusdt.depth.step0"}',
            '{"sub": "market.xrpusdt.depth.step0"}',
            '{"sub": "market.ltcusdt.depth.step0"}',
            '{"sub": "market.bchusdt.depth.step0"}',
            '{"sub": "market.eosusdt.depth.step0"}',
            '{"sub": "market.etcusdt.depth.step0"}',
            '{"sub": "market.ltcbtc.depth.step0"}',
            '{"sub": "market.bchbtc.depth.step0"}',
            '{"sub": "market.ethbtc.depth.step0"}',
            '{"sub": "market.eosbtc.depth.step0"}',
            '{"sub": "market.eoseth.depth.step0"}',
            '{"sub": "market.trxeth.depth.step0"}',
            '{"sub": "market.omgeth.depth.step0"}',
            '{"sub": "market.xmreth.depth.step0"}',
        ]

        for depthStr in depthStrs:
            ws.send(depthStr)

        while True:
            try:
                compressData = ws.recv()
                result = gzip.decompress(compressData).decode('utf-8')
                if result[:7] == '{"ping"':
                    ts = result[8:21]
                    pong = '{"pong":' + ts + '}'
                    ws.send(pong)
                    # ws.send('{"sub": "market.btcusdt.depth.step0"}')
                else:
                    # print('返回成功')
                    # print(result)
                    self.analys_pub(result)
            except Exception as e:
                logger.error('获取返回数据失败：　%s　' % e)
                break

    def analys_pub(self, data):
        try:
            code = ''
            item = json.loads(data)
            if 'tick' in item.keys():
                symbol = item['ch'][7:-12]
                if len(symbol) == 7:
                    code = symbol[:-4] + '_' + symbol[-4:]
                elif len(symbol) == 6:
                    code = symbol[:-3] + '_' + symbol[-3:]
                name = code.upper()
                timestamp = item['ts']
                bids = item['tick']['bids']
                asks = item['tick']['asks']

                asks_data = {
                    "price": sorted(asks, key=(lambda x: x[0]))[0][0],
                    "totalSize": sorted(asks, key=(lambda x: x[0]))[0][1]}
                bids_data = {
                    "price": sorted(bids, key=(lambda x: x[0]))[-1][0],
                    "totalSize": sorted(bids, key=(lambda x: x[0]))[-1][1]}

                # pub_data = /{
                #     'symbol': symbol,
                #     'price': sorted(asks, key=(lambda x: x[0]))[-1][0]
                # }

                if symbol == 'btcusdt':
                    if btcusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        btcusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'ethusdt':
                    if ethusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        ethusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))


                elif symbol == 'xrpusdt':
                    if xrpusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        xrpusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'ltcusdt':
                    if ltcusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        ltcusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'bchusdt':
                    if bchusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        bchusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))
               
                elif symbol == 'eosusdt':
                    if eosusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        eosusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'etcusdt':
                    if etcusdt.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        etcusdt.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'ltcbtc':
                    if ltcbtc.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        ltcbtc.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'bchbtc':
                    if bchbtc.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        bchbtc.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'ethbtc':
                    if ethbtc.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        ethbtc.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'eosbtc':
                    if eosbtc.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        eosbtc.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'eoseth':
                    if eoseth.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        eoseth.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'trxeth':
                    if trxeth.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        trxeth.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'omgeth':
                    if omgeth.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        omgeth.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

                elif symbol == 'xmreth':
                    if xmreth.get('price') != sorted(asks, key=(lambda x: x[0]))[0][0]:
                        xmreth.update(price=sorted(asks, key=(lambda x: x[0]))[0][0])
                        dataArr = {
                            "code": code,
                            "name": name,
                            "timestamp": timestamp,
                            "asks": asks_data,
                            "bids": bids_data,
                        }
                        # print(dataArr)
                        # redisConnect.set('vb:depth:newitem:' + str(code), json.dumps(dataArr))
                        redisConnect.publish('vb:depth:chan:ADEX', json.dumps(dataArr))

        except Exception as e:
            logger.error('处理数据失败: %s  ' % e)


if __name__ == '__main__':
    k = Teade_Data()
    k.spider()

# buy high

# sell low
