from loguru import logger
import os
import cx_Oracle
import datetime
import json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def insert_record():
    db100 = cx_Oracle.connect('swtonline', 'online', '192.168.1.100:1521/oradb')  # 连接100数据库swtonline/online@  192.168.1.100:1521/oradb
    print(db100.version)  # 打印版本看看
    logger.info('100库连接成功')
    cur100 = db100.cursor()
    sql1 = '''INSERT INTO
    SWTONLINE.TBL_DIRECT_POS_A
    (
        ACQ_INS_CODE,
        TRACE_NUM,
        TRANS_DATETIME,
        TRANS_KEY1,
        TRANS_KEY2,
        PROCESS_FLAG,
        REV_FLAG,
        TIPS_FLAG,
        BEFORE_TRANS_CODE,
        AFTER_TRANS_CODE,
        TRANS_CLASS,
        TRANS_CURR,
        BILLING_CURR,
        ACQ_SETT_CURR,
        STAT_CURR,
        CURR_EXPONENT,
        TRANS_AMT,
        BILLING_AMT,
        ACQ_SETT_AMT,
        STAT_AMT,
        TIPS_AMT,
        TRANS_RATE,
        ACQ_SETT_RATE,
        STAT_RATE,
        CONV_DATE,
        ACCT_NUM,
        CARD_SEQUENCE_NUM,
        ACQ_CARD_TIME,
        SETT_DATE,
        MER_TYPE,
        ACQ_CNTRY_CODE,
        ISSR_CNTRY_CODE,
        SRV_ENTRY_MODE,
        FWD_INS_CODE,
        RECV_INS_CODE,
        ISSR_INS_CODE,
        RETRIVL_REF_NUM,
        ORIG_AUTH_CODE,
        RESP_AUTH_CODE,
        RESP_CODE,
        TERM_ID,
        MER_CODE,
        TERM_BATCH_ID,
        TERM_TRACE_NUM,
        MER_ADDR_NAME,
        MER_ACQ_INS_CODE,
        ORIG_MSG,
        ADDTNL_AMT,
        SELF_DEFINE,
        SA_SAV1,
        SA_SAV2,
        REC_CREATE_TIME,
        REC_UPDATE_TIME,
        REC_CODE,
        REC_ID,
        CARD_STATE,
        F59
    )
    VALUES
    (
        '0848475210',
        '241079',
        TO_CHAR(SYSDATE,'MMDDHH24MISS'),
        '84758405712596291207264000'|| TO_CHAR(SYSDATE,'MMDDHH24MISS'),
        '012'|| TO_CHAR(SYSDATE,'MMDDHH24MISS'),
        '0',
        '0',
        '0',
        'PER',
        'PBI',
        'NRM',
        '156',
        '156',
        '156',
        '156',
        '2222',
        200000.65,
        0,
        200000.65,
        0,
        0,
        '90000000',
        '90000000',
        '0',
        '1',
        '196222531314232847456',
        '001',
        '0123230006',
        TO_CHAR(SYSDATE,'YYYYMMDD'),
        '3525',
        '020',
        '000',
        '051',
        '0800000001',
        '0814505800',
        '0814505800',
        '191'||TO_CHAR(systimestamp,'HH24MISSFF3'),
        '  ',
        '  ',
        '00',
        '92210821',
        '847100072100008',
        '000067',
        '000761',
        '深圳市红宝电器',
        '0848475840',
        '  ',
        '0401001156C0000001542711002156C000000154271',
        '002U00','603100010230',
        '0101',
        SYSDATE,
        SYSDATE,
        '012222100369960',
        '',
        '02107011',
        ''
    )'''
    cur100.execute(sql1)
    db100.commit()
    db62 = cx_Oracle.connect('swtonline', 'swtonline', '192.168.2.62:1521/chinapay')  # 连接62数据库
    print(db62.version)  # 打印版本看看
    logger.info('62库连接成功')
    cur = db62.cursor()  # 游标操作
    sql = "insert into TBL_WITHDRAW_CASH_FEE (WITHDRAW_ID, MER_CODE, MER_NAME, TRAN_AMT, WITHDRAW_CASH_VALUE, MAX_WITHDRAW_CASH_VALUE, MER_COMMISION_VALUE, MAX_MER_COMMISION_VALUE, TRAN_DATE, WITHDRAW_DATE, MERCHANT_STATE, OUT_FEE_STATE, AMOUNT, SETT_AMT, BATCH_NO, TERM_CODE, OUT_STATE, AUDITING_STATE, REDUCTIONMONEY, REMARK_STR, AUDITING_DATE_TIME, OUT_FEE_DATE_TIME, PROXYPROFIT, ZF_PROFIT, PROXY_SPLITTING_TX, ADDR_IP, SIGN_STATE, MER_CODE_KQ, MER_FEE, MER_FEE_RATE, WITHDRAW_CASH_VALUE_OVER, PICTURE_STATE, APPROVER, SPEED_STATE, CERTIFICATION_FEE, OUT_WAY, REMARKSTR2, FLAG, COLLECT_FEE, FLAG_STR, ISAUTO, ISFIND, ISTHREAD, IS_FIND_THREAD, TRADE_COMMISION_VALUE, TRADE_AMOUNT, RETURN_AMT, RETRIVL_REF_NUM, SERIAL_NO, CARD_TYPE, STAT_RATE, BRAND_SERVICE_RATE, BRAND_WITHDRAW_CHARGE, CONV_DATE, IS_DELAYED)" \
          "values (TBL_WITHDRAW_CASH_FEE_ID.Nextval, '847100072100008', 'T1 test of traditional POS personal computer business district 008', 20,2, 1999, 0.04, 0, to_char(sysdate,'YYYY-MM-DD'),to_char(sysdate,'YYYY-MM-DD HH24:MI:SS'), '1', '1', 0.04, 200, '', null, '02', '01', 0, '【风控_：@通过11:40:59】',to_char(sysdate,'YYYY-MM-DD HH24:MI:SS'), null, 0, 0.04, 0, '192.168.18.232', '0', null, 0, 0, 0, null, '风控_', null, 0, null, null, null, 0, '0', '', '', '', '0', 0, 0, 0, null, 'SDTX20190312'||TestData.Nextval||'SLR', null, null, 0, 0, null, '0')"
    cur.execute(sql)
    db62.commit()
    cur.execute("select max(WITHDRAW_ID) from TBL_WITHDRAW_CASH_FEE where MER_CODE='847100072100008' order by WITHDRAW_ID desc")
    Embody_record = cur.fetchall()
    result =Embody_record
    logger.info(Embody_record)
    WITHDRAW_ID = result[0][0]
    TRAN_DATE = result[95:105]
    SETT_AMT = result[147:156]
    MER_CODE = result[13:28]
    TransactionData = {
        "WITHDRAW_ID":WITHDRAW_ID,
        "TRAN_DATE":TRAN_DATE,
        "SETT_AMT":SETT_AMT,
        "MER_CODE":MER_CODE

    }
    logger.info(WITHDRAW_ID)
    return WITHDRAW_ID
insert_record()