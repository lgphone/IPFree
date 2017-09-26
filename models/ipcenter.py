#!/usr/bin/python3
import pymysql.cursors
from config import DB_CONF


class DB():
    def init_conn(self):
        self.conn = pymysql.connect(host=DB_CONF['host'],
                                    user=DB_CONF['user'],
                                    password=DB_CONF['password'],
                                    db=DB_CONF['db'],
                                    charset=DB_CONF['charset'],
                                    cursorclass=pymysql.cursors.DictCursor)

    def re_conn(self):
        while 1:
            try:
                if self.conn.ping():
                    return self.conn
            except Exception as e:
                print('连接错误:{_e} 重新连接'.format(_e=e))
                self.init_conn()
                return self.conn

    def close_conn(self):
        if self.conn.ping():
            self.conn.close()

DBdrive = DB()

def exec_query_ip(ip='127.0.0.1'):
    ret = {'status': True,
           'data': ''}
    try:
        with DBdrive.re_conn().cursor() as cursor:
            sql = "SELECT * FROM `aiwen_free_district_v2.0.1` WHERE minip <= INET_ATON('{_query_ip}') ORDER BY minip DESC LIMIT 1;".format(_query_ip=ip)
            cursor.execute(sql)
            result = cursor.fetchone()
            ret['data'] = result
    except Exception as e:
        print('error', e)
        ret['status'] = False
    finally:
        return ret
