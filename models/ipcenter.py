#!/usr/bin/python3
import pymysql.cursors
from config import DB_CONF

connection = pymysql.connect(host=DB_CONF['host'],
                             user=DB_CONF['user'],
                             password=DB_CONF['password'],
                             db=DB_CONF['db'],
                             charset=DB_CONF['charset'],
                             cursorclass=pymysql.cursors.DictCursor)


def exec_query_ip(ip='127.0.0.1'):
    ret = {'status': True,
           'data': ''}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `aiwen_free_district_v2_0_4` WHERE minip <= INET_ATON('{_query_ip}') ORDER BY minip DESC LIMIT 1;".format(_query_ip=ip)
            cursor.execute(sql)
            result = cursor.fetchone()
            ret['data'] = result
    except Exception as e:
        print('error', e)
        ret['status'] = False
    finally:
        return ret
