==>����ģ�� /* *.redis.yml */<==
R_Host_Port: 127.0.0.1:6379
# Ĭ�����ݿ�
R_DB: 0
# ���Ŀ���������
R_MaxIdle: 1
# ��ʱ��λ��
R_IdleTimeout: 180
# ��ʱ��λ��
R_DialConnectTimeout: 30
# ��ʱ��λ��
R_DialReadTimeout: 120



==>����ģ�� /* hb.wscli.conf.yml */<==
# WssUriֵ���ɸı�
WssUri: wss://www.huobi.com/-/s/pro/ws
# ToChansParams���ɸı�
ToChansParams:
    #toChannelA: ���ݽ����͵�toChannelA��
    toChannelA:
        #groupA: ���飬������ÿ�齨��һ��websocket����
        groupA:
            #subkeyA: �������ݵ�ָ���ʽ��Ϊtrue���ģ���֮�����ģ�
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

            
            
==>����ģ�� /* chanser.conf.yml */<==
# �����IP
ServerIP: 127.0.0.1
# �����˿�
ServerPort: 8058
# �Ƿ���IP���ˣ�true: ����
AllowIPsON: true
# �����¼��IP�������|�ָ�
AllowedIPs: 127.0.0.1|ip1|ip2
# BytesChans���ɸı�: ��Ч����ͨ��
BytesChans:
    #Chan1-Md5: �ͻ��˴���Ķ���Key����dataType_BytesChan1����ͨ���е����ݷ������ĵĿͻ��ˣ�
    Chan1-Md5: dataType_BytesChan1
    Chan2-Md5: dataType_BytesChan2
    Chan3-Md5: dataType_BytesChan3
    Chan4-Md5: dataType_BytesChan4
    Chan5-Md5: dataType_BytesChan5