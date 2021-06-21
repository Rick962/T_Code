==>配置模版 /* *.redis.yml */<==
R_Host_Port: 127.0.0.1:6379
# 默认数据库
R_DB: 0
# 最大的空闲连接数
R_MaxIdle: 1
# 超时单位秒
R_IdleTimeout: 180
# 超时单位秒
R_DialConnectTimeout: 30
# 超时单位秒
R_DialReadTimeout: 120



==>配置模版 /* hb.wscli.conf.yml */<==
# WssUri值不可改变
WssUri: wss://www.huobi.com/-/s/pro/ws
# ToChansParams不可改变
ToChansParams:
    #toChannelA: 数据将推送到toChannelA中
    toChannelA:
        #groupA: 分组，组名；每组建立一个websocket连接
        groupA:
            #subkeyA: 订阅数据的指令格式；为true则订阅，反之不订阅；
            subkeyA: true
            subkeyB: true
        groupB:
            subkeyA: true
            subkeyB: true

    toChannelB:
        groupA:
            subkeyA: true
            subkeyB: true
        groupB:
            subkeyA: true
            subkeyB: true

            
            
==>配置模版 /* chanser.conf.yml */<==
# 服务端IP
ServerIP: 127.0.0.1
# 监听端口
ServerPort: 8058
# 是否开启IP过滤；true: 开启
AllowIPsON: true
# 允许登录的IP；多个用|分割
AllowedIPs: 127.0.0.1|ip1|ip2
# BytesChans不可改变: 有效数据通道
BytesChans:
    #Chan1-Md5: 客户端传入的订阅Key；将dataType_BytesChan1数据通道中的数据返给订阅的客户端；
    Chan1-Md5: dataType_BytesChan1
    Chan2-Md5: dataType_BytesChan2
    Chan3-Md5: dataType_BytesChan3
    Chan4-Md5: dataType_BytesChan4
    Chan5-Md5: dataType_BytesChan5