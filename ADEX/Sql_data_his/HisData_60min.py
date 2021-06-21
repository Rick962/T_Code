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
        url = 'https://api.huobi.vn/market/history/kline?period=60min&size=20&symbol=' + str(sm)
        res = requests.get(url).text
        return res

    def main(self):
        code = ''
        while True:
            time.sleep(9)
            symbols = ['btcusdt', 'ethusdt', 'xrpusdt','ltcusdt', 'bchusdt', 'eosusdt','etcusdt', 'ltcbtc', 'bchbtc', 'ethbtc', 'eosbtc', 'eoseth',
                       'trxeth', 'omgeth', 'xmreth',
                       ]
            for symbol in symbols:
                datas = self.spider(symbol)
                data = json.loads(datas)
                if data.get('ch'):
                    symbol_list = ['btcusdt', 'ethusdt', 'xrpusdt',
                                   'ltcbtc', 'bchbtc', 'xxx', 'eosbtc', 'eoseth',
                                   'trxeth', 'omgeth', 'xmreth', 'adexusdt', 'xxx', 'ethbtc','ltcusdt', 'bchusdt', 'eosusdt','etcusdt',]
                    pid = (int(symbol_list.index(symbol)) + 1)
                    if len(symbol) == 7:
                        code = symbol[:-4] + '_' + symbol[-4:]
                    elif len(symbol) == 6:
                        code = symbol[:-3] + '_' + symbol[-3:]
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
                    logger.error('%s 数据获取失败' % symbol)
            time.sleep(3000)
        return

    def write_db(self, data):
        try:
            insert_sql = "REPLACE INTO xy_60min_info(pid, timestamp, openingPrice, closingPrice, " \
                         "lowestPrice, highestPrice, volume, dateTime, date, time, code, name) " \
                         "VALUES (%d,'%s', %.6f, %.6f, %.6f, %.6f, %.6f, '%s', '%s', '%s', '%s', '%s')"
            cur.execute(insert_sql % (data))
            cur_conn.commit()
            # print(insert_sql % data)
        except EOFError as e:
            logger.error('write error: %s ', e)
        return

    def create_tb(self, data):
        try:
            con = pymysql.connect("localhost", "root", "zxc", charset='utf8')
            cur = con.cursor()
            create_db = 'create database if not exists HuoBi;'
            cur.execute(create_db)
            s_db = 'use HuoBi;'
            cur.execute(s_db)
            c_tb = """
               CREATE TABLE if not exists `xy_dayk_info` (
                  `id` int(32) NOT NULL AUTO_INCREMENT,
                  `pid` int(11) DEFAULT NULL COMMENT '商品ID',
                  `code` varchar(32) DEFAULT NULL COMMENT 'eg: btcusdt',
                  `name` varchar(32) DEFAULT NULL COMMENT 'eg: BTC_USDT',
                  `openingPrice` varchar(255) DEFAULT NULL COMMENT '开盘价',
                  `closingPrice` varchar(255) DEFAULT NULL COMMENT '收盘价',
                  `highestPrice` varchar(255) DEFAULT NULL COMMENT '最高价',
                  `lowestPrice` varchar(255) DEFAULT NULL COMMENT '最低价',
                  `volume` varchar(255) DEFAULT NULL COMMENT '成交量',
                  `date` date DEFAULT NULL COMMENT '日期',
                  `time` varchar(20) DEFAULT NULL COMMENT '时间',
                  `dateTime` datetime DEFAULT NULL COMMENT '日期时间',
                  `timestamp` int(11) DEFAULT NULL COMMENT '时间戳',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `code` (`code`,`date`,`time`) USING BTREE
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='1min信息表';
               """
            cur.execute(c_tb)
            insert_sql = 'INSERT IGNORE INTO btcusdt_1min(ids, openingPrice, closingPrice, lowestPrice, highestPrice, amount, volume, count) ' \
                         'VALUES ("%d", %.6f, %.6f, %.6f, %.6f, %.6f, %.6f, %.6f)'
            cur.execute(insert_sql % data)

            cur.close()
            print('close cur')
            con.close()
            print('colose connect DB')


        except:
            print('Failure to connect database')

    def close_db(self):
        cur = pymysql.connect("localhost", "root", "zxc", charset='utf8').cursor()
        cur.close()
        print('close cur')
        pymysql.connect("localhost", "root", "zxc", charset='utf8').close()
        print('colose connect DB')


f = Func()
f.main()
cur.close()
