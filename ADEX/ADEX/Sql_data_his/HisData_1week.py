import os
import sys
import json
import time
import requests
import pymysql
import logging.config

sys.path.append(os.path.dirname(os.getcwd()))

from until.log_setting import logconfig

logging.config.dictConfig(logconfig)
logger = logging.getLogger(__name__)

cur_conn = pymysql.connect(host="47.244.176.182",
                           user="root",
                           password="3aG6N72FiJ$w*M7C",
                           database='adex',
                           charset='utf8')

cur = cur_conn.cursor()


class Func:
    def spider(self, sm):
        time.sleep(4)
        url = 'https://api.huobi.vn/market/history/kline?period=1week&size=7&symbol=' + str(sm)
        res = requests.get(url).text
        return res

    def main(self):
        code = ''
        while True:
            time.sleep(50)
            symbols = ['btcusdt', 'ethusdt', 'xrpusdt','ltcusdt', 'bchusdt', 'eosusdt', 'etcusdt', 'ltcbtc', 'bchbtc', 'ethbtc', 'eosbtc', 'eoseth',
                       'trxeth', 'omgeth', 'xmreth',
                       ]
            for sm in symbols:
                datas = self.spider(sm)
                data = json.loads(datas)
                if data.get('ch'):
                    symbol_list = ['btcusdt', 'ethusdt', 'xrpusdt',
                                   'ltcbtc', 'bchbtc', 'xxx', 'eosbtc', 'eoseth',
                                   'trxeth', 'omgeth', 'xmreth', 'adexusdt', 'xxx', 'ethbtc', 'ltcusdt', 'bchusdt', 'eosusdt','etcusdt',]
                    pid = (int(symbol_list.index(sm)) + 1)
                    if len(sm) == 7:
                        code = sm[:-4] + '_' + sm[-4:]
                    elif len(sm) == 6:
                        code = sm[:-3] + '_' + sm[-3:]
                    name = code.upper()
                    for item in data['data']:
                        self.write_db(
                            (pid, str(item['id']), float(item['open']), float(item['close']), float(item['low']),
                             float(item['high']),
                             float(item['amount']),
                             str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['id']))),
                             str(time.strftime("%Y-%m-%d", time.localtime(item['id']))),
                             str(time.strftime("%H:%M:%S", time.localtime(item['id']))), str(code), str(name)
                             ))
                else:
                    logger.error('%s 数据获取失败' % sm)
            time.sleep(1100)
        return

    def write_db(self, data):
        try:
            insert_sql = "REPLACE INTO xy_week_info(pid, timestamp, openingPrice, closingPrice, " \
                         "lowestPrice, highestPrice, volume, dateTime, date, time, code, name) " \
                         "VALUES (%d,'%s', %.6f, %.6f, %.6f, %.6f, %.6f, '%s', '%s', '%s', '%s', '%s')"
            cur.execute(insert_sql % (data))
            cur_conn.commit()
            # print(insert_sql % data)
        except EOFError as e:
            logger.error('write error: %s ', e)
        return


f = Func()
f.main()
cur.close()
